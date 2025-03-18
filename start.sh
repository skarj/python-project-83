#!/usr/bin/env bash

source $HOME/.local/bin/env
gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app