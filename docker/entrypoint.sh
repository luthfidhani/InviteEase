#!/usr/bin/env sh
set -e

# Inisiasi project kalau pertama kali container dijalankan
if [ ! -f /app/manage.py ]; then
  django-admin startproject inviteease .
fi

python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

# Jalankan ASGI via Daphne
exec daphne -b 0.0.0.0 -p 8000 inviteease.asgi:application
