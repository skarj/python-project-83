#!/usr/bin/env bash

PORT=8080

source $HOME/.local/bin/env
uv run gunicorn -w 5 -b 0.0.0.0:$PORT page_analyzer:app
