#!/usr/bin/env bash
echo "curl -s -I localhost | head -n 1 | grep 200 >/dev/null"
curl -s -I localhost | head -n 1 | grep 200 >/dev/null || docker ps -a
