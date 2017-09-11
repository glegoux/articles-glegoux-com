#!/usr/bin/env bash
#
# httpserver.sh
#
# usage: bash httpserver.sh [IP_ADDRESS] [PORT]
#        By default it serves HTTP on 127.0.0.1 port 8000.
#
# Run python HTTP server.

IP_ADDRESS=${1:-127.0.0.1}
PORT=${2:-8000}

python3 -m http.server "${PORT}" --bind "${IP_ADDRESS}"
