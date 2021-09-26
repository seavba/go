#!/usr/bin/env bash
curl -s -I localhost | head -n 1 | grep 200 >/dev/null
