#!/usr/bin/env sh
set -eu
python3 tools/catalog.py validate
python3 -m unittest discover -s tests -v
