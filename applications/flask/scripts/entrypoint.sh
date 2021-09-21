#!/bin/sh
set -euo pipefail

echo "Working directory: ${PWD}"
if [ "$1" == uwsgi ]; then
    echo "Activate venv"
    source venv/bin/activate
    # echo "DB upgrade"
    # python3 ./manage.py db upgrade
    # python3 ./init_if_needed.py
    exec "$@"

else
    exec "$@"
fi