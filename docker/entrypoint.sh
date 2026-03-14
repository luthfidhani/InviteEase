#!/usr/bin/env sh
set -e

# Render (dan banyak PaaS) mengatur PORT; wajib listen di sini agar health check lolos
PORT="${PORT:-8000}"

# Inisiasi project kalau pertama kali container dijalankan
if [ ! -f /app/manage.py ]; then
  django-admin startproject inviteease .
fi

# SQLite butuh direktori data/ ada (tanpa DATABASE_URL)
mkdir -p /app/data

python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

# ASGI via Daphne — bind ke PORT (Render: biasanya 10000)
exec daphne -b 0.0.0.0 -p "$PORT" inviteease.asgi:application
