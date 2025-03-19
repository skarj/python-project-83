#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install

# TODO: fix
uv pip compile pyproject.toml -o requirements.txt
pip install -r requirements.txt
