#!/bin/bash
set -xe

echo "Working directory: ${PWD}"
if [ "$1" == uwsgi ]; then
    echo "Activate venv"
    . venv/bin/activate
    exec "$@"

else
    exec "$@"
fi