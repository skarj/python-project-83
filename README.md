[![Maintainability](https://api.codeclimate.com/v1/badges/e3ca9c69384cf7c1a059/maintainability)](https://codeclimate.com/github/skarj/python-project-50/maintainability)x
[![Actions Status](https://github.com/skarj/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/skarj/python-project-83/actions)

# Page Analyzer
[Page Analyzer](https://python-project-83-yclu.onrender.com/) is a site that analyzes the specified pages for SEO suitability, similar to [PageSpeed ​​Insights](https://pagespeed.web.dev/):

## Access
Application is deployed to [render.com](https://render.com/)
[Page Analyzer](https://python-project-83-yclu.onrender.com/)

## Requirements
Python 3.10+

## Local Installation
### Clone repository
```bash
git clone https://github.com/skarj/python-project-83.git
cd python-project-83
make install # Install dependencies
make build # Buld package
```

### Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### Install application
```bash
make install
```

### Put secrets to .env file
```
echo SECRET_KEY="{flask_secret_key}"
echo DB_URL="postgresql://{user}:{password}@127.0.0.1:5432/sites"
```

### Start local Postgresql database
```
docker run --name postgres16 \
  -e POSTGRES_USER=appuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=sites \
  -p 5432:5432 \
  -d postgres:16

psql -a -d $DB_URL -f database.sql
```

### Start development application
```
make dev
```
