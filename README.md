# InviteEase 🎉

A lightweight self-hosted **guest check-in system** built with **Django + Channels + Bootstrap 5**. Ideal for weddings, corporate events, or any place where you need a fast, paper-less reception desk.

---

## ✨ Features

| Module | What it does |
|--------|--------------|
| **Desk** (`/desk/<id>/`) | • Manual search & check-in
.| • QR / barcode scanning via device camera |
| **Screen** (`/screen/<id>/`) | • Full-screen welcome splash  
.| • Realtime updates (WebSocket)  
.| • Auto-fade after 6 s |
| **Admin** (`/admin/`) | • CRUD guests  
.| • CSV import/export  
.| • Filters & search |
| **Dockerized** | One-command deploy; SQLite by default or **Supabase (Postgres)** via `DATABASE_URL` |

---

## 🐳 Quick Start (Docker)

1. **Clone the repo**
```bash
$ git clone https://github.com/luthfidhani/InviteEase.git && cd InviteEase
```
2. **Copy environment sample & tweak SECRET_KEY**
```bash
$ cp .env.example .env
```
3. **Build and run**
```bash
$ make build
$ make up
```
4. **Create an admin user (first run only)**
```bash
$ make createsuperuser
```

**Login aplikasi**  
Dashboard, Desk, dan Guest List membutuhkan login. Buat user di **Admin → Users → Add user**: isi username/password, **jangan centang "Staff status"** — user itu bisa pakai app tapi **tidak bisa** buka `/admin/`. Yang mengelola tamu & user staff tetap pakai akun superuser/staff.

**Screen** (`/screen/<id>/`) tetap **tanpa login** agar TV bisa buka langsung.

Open:
- **Desk** → http://localhost:8000/desk/1/
- **Screen** → http://localhost:8000/screen/1/

> 🖥️ **Desk `<id>` always syncs to Screen `<id>`**  
> Example: Desk 1 updates Screen 1, Desk 2 updates Screen 2, etc.

> 📱 **Desk is recommended to be accessed using mobile devices (smartphones/tablets)**  
> Reason: Mobile devices allow flexibility for receptionists to move around, scan QR codes with the built-in camera, and type guest names easily.

> 🖥️ **Screen should be displayed on larger monitors or TVs**  
> Reason: Ensures clear, visible welcome messages for guests across the room, providing a professional and engaging experience.
- **Admin** → http://localhost:8000/admin/

> 📱 On mobile devices, use the LAN IP instead of `localhost`.

---

## 🖥️ Run Without Docker

1. **Install [uv](https://github.com/astral-sh/uv)**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Sync dependencies & create virtual environment**:

```bash
uv sync
```

3. **Activate virtual environment**:

```bash
source .venv/bin/activate
```

4. **Run Daphne ASGI server**:

```bash
daphne -b 0.0.0.0 -p 8000 inviteease.asgi:application
```

5. Access the app at http://localhost:8000/

---

## 🛠️ Project Structure

```
inviteease/
├─ compose.yml              # Docker services
├─ docker/
│  ├─ Dockerfile            # Image (Python + Daphne + WhiteNoise)
│  └─ entrypoint.sh         # migrate ➜ collectstatic ➜ serve
├─ inviteease/              # Django project settings
├─ guests/                  # Domain app (models, views, WS consumers)
└─ data/                    # SQLite volume & staticfiles
```

---

## 📦 Environment Variables

| Var | Default | Note |
|-----|---------|------|
| `DEBUG` | `1` | Set `0` in production |
| `SECRET_KEY` | `change-me` | Django secret—**change it!** |
| `ALLOWED_HOSTS` | `*` | Comma-separated list |
| `CSRF_TRUSTED_ORIGINS` |  | Add your ngrok / domain if using HTTPS proxy |
| `DATABASE_URL` | *(empty)* | If set, uses **Supabase / PostgreSQL** instead of SQLite |
| `PORT` | `8000` | Di **Render**, platform set otomatis (mis. `10000`) — entrypoint sudah pakai ini |

---

## Deploy ke Render (Docker)

1. **Dockerfile path:** `docker/Dockerfile` (bukan root).
2. **Environment variables wajib / disarankan:**
   - `SECRET_KEY` — random panjang
   - `DEBUG=0`
   - `ALLOWED_HOSTS` — hostname Render kamu, mis. `inviteease.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` — `https://inviteease.onrender.com`
   - `DATABASE_URL` — dari **Render PostgreSQL** (disarankan; tanpa ini pakai SQLite di disk ephemeral)
   - `DATABASE_FORCE_IPV4=0` — di Render jangan paksa IPv4 (bisa putus SSL / koneksi Postgres)
3. **Jangan** isi **Docker Command** dengan perintah yang bentrok; biarkan default **ENTRYPOINT** (`entrypoint.sh` sudah `migrate` + `daphne` di **`$PORT`**).

Kalau deploy masih gagal, buka **Logs** di dashboard Render — baris error Python/shell muncul sebelum exit.

---

## Supabase (PostgreSQL)

Supabase is managed Postgres. InviteEase stays the same; only the DB backend changes.

1. **Create a project** at [supabase.com](https://supabase.com) → wait until the DB is ready.
2. **Connection string**  
   **Project Settings → Database**  
   - Prefer **URI** with **Direct connection** (port **5432**) or **Session pooler** on **5432** for Django (migrations need a session-capable connection).  
   - Avoid **Transaction** pooler (6543) for `migrate`; if you must use 6543, set Session mode in Supabase or run migrations against direct 5432.
3. **`.env`**
   ```bash
   DATABASE_URL=postgresql://postgres.[ref]:YOUR_PASSWORD@aws-0-REGION.pooler.supabase.com:5432/postgres
   ```
   Special characters in the password must be URL-encoded (e.g. `@` → `%40`).
4. **Install deps** (includes `psycopg2-binary`): `uv sync`
5. **Apply schema**
   ```bash
   python manage.py migrate
   ```
6. **Admin user**: `python manage.py createsuperuser`
7. **Data from old SQLite** (optional): export with `dumpdata`, or use a one-off SQLite→Postgres tool; fresh deploys often start empty and re-import CSV from Admin.

If `DATABASE_URL` is **not** set, the app still uses SQLite under `data/db.sqlite3`.

**WSL2 / "Network is unreachable"**  
Supabase DNS sering mengembalikan IPv6 dulu; banyak setup WSL2 tidak punya route IPv6 ke internet. InviteEase secara default memaksa koneksi lewat **IPv4** (`DATABASE_FORCE_IPV4=1`). Kalau perlu matikan: `DATABASE_FORCE_IPV4=0` di `.env`.

---

## 🔧 Local Development

**Start services with live reload**
```bash
docker compose up -d
```
**Run tests**
```bash
make test
```
**Generate migrations**
```bash
make makemigrations && make migrate
```

WhiteNoise auto-refresh is enabled while `DEBUG=1`, so static changes reflect immediately.

---

## 🌐 Deployment Notes

| Scenario | Recommendation |
|----------|----------------|
| **Offline LAN** | Keep defaults, serve via IP address |
| **Public HTTPS** | Put Nginx / Caddy in front, or add Let’s Encrypt certs |
| **Scaling** | Swap `InMemoryChannelLayer` → Redis; use Supabase via `DATABASE_URL` for Postgres |

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

> Made with ❤️ by Luthfi — may your guests feel truly welcomed!

## Screenshots
### Dashboard
![Dashboard](screenshots/1.png)

### Guest List
![Guest List](screenshots/2.png)

### Check-in Desk
![Check-in Desk](screenshots/3.png)

### Display Screen
![Display Screen](screenshots/4.png)

### Admin Panel
![Admin Panel](screenshots/5.png)

