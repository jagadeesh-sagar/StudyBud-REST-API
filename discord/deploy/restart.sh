#!/bin/bash
set -e

# Example for a Python app (Django/Flask). Adjust if Node/Go/etc.
APP_DIR=/srv/myapp

cd "$APP_DIR"

# optional: python deps
if command -v python3 >/dev/null 2>&1; then
  python3 -m venv .venv || true
  source .venv/bin/activate
  if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt || true
  fi
fi

# migrate / collectstatic if needed (Django)
# python manage.py migrate --noinput || true
# python manage.py collectstatic --noinput || true

# restart your service
systemctl restart myapp || systemctl start myapp
