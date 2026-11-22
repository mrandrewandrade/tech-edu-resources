#!/usr/bin/env bash

set -eu

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
python_dir="$(CDPATH= cd -- "$script_dir/../python" && pwd)"

cd "$python_dir"
python3 -m unittest discover -s tests -v
python3 -m compileall -q .
