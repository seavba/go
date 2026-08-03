# Registro de glucemia

Datos en `glucemia_log.json`. Cada apunte se commitea y se pushea.

`gen_tabla.py` genera `tabla_glucemia.html` a partir del JSON. `gen_pdf.sh`
lo regenera y lo imprime a `glucemia.pdf` con Chromium headless.

## Comandos

| Comando | Efecto |
|---|---|
| `apunta <valor>` | Registra el valor con la fecha y hora actuales |
| `apunta <valor> y alarma` | Registra el valor **y** crea el evento de recordatorio |
| `alarma` | Crea el evento para el último valor registrado |
| `dame tabla` | Muestra el histórico completo en una tabla |
| `pdf` | Genera `glucemia.pdf` con el histórico completo y lo envía |

`apunta <valor> y alarma` y la secuencia `apunta <valor>` → `alarma` son equivalentes.

## Hora

Las horas se registran en **CEST** (`Europe/Madrid`, UTC+2 en verano). El sistema
corre en UTC, así que a la hora del sistema se le suman las 2 horas antes de
guardarla.

## Evento de recordatorio

- Título: `Test glucemia`
- Cuándo: 2 horas después del apunte
- Calendario: `sergio@cloudify.consulting`
- Invitado: `avi.muque@gmail.com`
- Avisos: 10 min antes, 5 min antes, y a la hora
- Zona horaria: `Europe/Madrid`

## Aviso en el iPhone

La notificación de Google Calendar no es una alarma: suena una vez y **no suena
en modo silencio**. Para un aviso real:

- **Tono largo**: añadir la cuenta de Google a la app Calendario de Apple
  (Ajustes → Apps → Calendario → Cuentas) y elegir un tono de llamada en
  Ajustes → Sonidos y hápticos → Alertas de calendario.
- **Alarma de verdad**: atajo de Atajos con la acción "Iniciar temporizador" de
  2 horas, lanzado con "Oye Siri, glucemia". Hay que dispararlo desde el
  iPhone; no se puede activar en remoto.
