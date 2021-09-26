#!/usr/bin/env bash
sleep 10
curl -s -I localhost | head -n 1 | grep 200 >/dev/null || docker ps -a
curl -i localhost
