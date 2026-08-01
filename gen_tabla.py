#!/usr/bin/env python3
"""Genera la tabla HTML de glucemias a partir de glucemia_log.json."""

import json
import sys
from pathlib import Path

REPO = Path(__file__).parent
LOG = REPO / "glucemia_log.json"


def flag(valor):
    """Marca solo los extremos. Sin contexto (ayunas / postprandial) no se
    puede clasificar un valor intermedio, así que no se clasifica."""
    if valor < 70:
        return ("baja", "Baja")
    if valor > 180:
        return ("alta", "Alta")
    return ("", "")


def main():
    registros = json.loads(LOG.read_text())
    if not registros:
        print("Sin registros", file=sys.stderr)
        return 1

    registros = sorted(registros, key=lambda r: (r["fecha"], r["hora"]))
    valores = [r["valor"] for r in registros]

    filas = []
    for r in registros:
        clase, etiqueta = flag(r["valor"])
        marca = f'<span class="flag {clase}">{etiqueta}</span>' if etiqueta else ""
        filas.append(
            f"<tr><td>{r['fecha']}</td><td>{r['hora']}</td>"
            f"<td class=\"num\">{r['valor']}</td><td>{marca}</td></tr>"
        )

    html = TEMPLATE.format(
        total=len(registros),
        ultimo=valores[-1],
        media=round(sum(valores) / len(valores)),
        minimo=min(valores),
        maximo=max(valores),
        filas="\n".join(filas),
    )
    (REPO / "tabla_glucemia.html").write_text(html)
    return 0


TEMPLATE = """<title>Registro de glucemia</title>
<style>
  :root {{
    --bg: #fbfbfa; --fg: #1a1a1a; --muted: #6b6b6b;
    --line: #e4e4e0; --card: #fff; --accent: #3d5a80;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #16181d; --fg: #e8e8e6; --muted: #9a9a96;
      --line: #2c2f36; --card: #1d2026; --accent: #8fb0d9;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #16181d; --fg: #e8e8e6; --muted: #9a9a96;
    --line: #2c2f36; --card: #1d2026; --accent: #8fb0d9;
  }}
  :root[data-theme="light"] {{
    --bg: #fbfbfa; --fg: #1a1a1a; --muted: #6b6b6b;
    --line: #e4e4e0; --card: #fff; --accent: #3d5a80;
  }}
  body {{
    background: var(--bg); color: var(--fg); margin: 0;
    font: 16px/1.5 ui-sans-serif, -apple-system, system-ui, sans-serif;
    padding: 2rem 1.25rem;
  }}
  main {{ max-width: 46rem; margin: 0 auto; }}
  h1 {{ font-size: 1.4rem; font-weight: 600; margin: 0 0 1.5rem; }}
  .stats {{
    display: grid; gap: .75rem; margin-bottom: 2rem;
    grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr));
  }}
  .stat {{
    background: var(--card); border: 1px solid var(--line);
    border-radius: .5rem; padding: .75rem .9rem;
  }}
  .stat dt {{
    font-size: .7rem; letter-spacing: .04em; text-transform: uppercase;
    color: var(--muted); margin: 0 0 .25rem;
  }}
  .stat dd {{ margin: 0; font-size: 1.5rem; font-weight: 600; font-variant-numeric: tabular-nums; }}
  .wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }}
  th {{
    text-align: left; font-size: .72rem; letter-spacing: .04em;
    text-transform: uppercase; color: var(--muted); font-weight: 600;
    padding: 0 .75rem .5rem 0; border-bottom: 1px solid var(--line);
  }}
  td {{ padding: .6rem .75rem .6rem 0; border-bottom: 1px solid var(--line); }}
  td.num {{ font-weight: 600; }}
  th:last-child, td:last-child {{ padding-right: 0; }}
  .flag {{
    font-size: .72rem; padding: .15rem .5rem; border-radius: 1rem;
    background: #f0e6d2; color: #6b4e12;
  }}
  .flag.baja {{ background: #dbe7f3; color: #1e3f66; }}
  .flag.alta {{ background: #f3ddd9; color: #7a2e20; }}
  @media (prefers-color-scheme: dark) {{
    .flag.baja {{ background: #1e2f45; color: #a8c8e8; }}
    .flag.alta {{ background: #3d2320; color: #e8a89a; }}
  }}
  p.nota {{
    margin-top: 1.5rem; font-size: .82rem; color: var(--muted);
    border-top: 1px solid var(--line); padding-top: 1rem;
  }}
</style>
<main>
  <h1>Registro de glucemia</h1>
  <dl class="stats">
    <div class="stat"><dt>Registros</dt><dd>{total}</dd></div>
    <div class="stat"><dt>Último</dt><dd>{ultimo}</dd></div>
    <div class="stat"><dt>Media</dt><dd>{media}</dd></div>
    <div class="stat"><dt>Mínimo</dt><dd>{minimo}</dd></div>
    <div class="stat"><dt>Máximo</dt><dd>{maximo}</dd></div>
  </dl>
  <div class="wrap">
    <table>
      <thead>
        <tr><th>Fecha</th><th>Hora (CEST)</th><th>mg/dL</th><th></th></tr>
      </thead>
      <tbody>
{filas}
      </tbody>
    </table>
  </div>
  <p class="nota">
    Solo se marcan los extremos (&lt;70 y &gt;180). Los valores intermedios no
    se clasifican: sin saber si la medición es en ayunas o después de comer, la
    misma cifra puede ser normal o no.
  </p>
</main>
"""


if __name__ == "__main__":
    sys.exit(main())
