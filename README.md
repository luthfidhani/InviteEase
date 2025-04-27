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
| **Dockerized** | One-command deploy with SQLite volume |

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
| **Scaling** | Swap `InMemoryChannelLayer` → Redis, mount Postgres instead of SQLite |

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

> Made with ❤️ by Luthfi — may your guests feel truly welcomed!

## Screenshot
![image](https://github.com/user-attachments/assets/c8a005a5-e3ee-4a08-b0ad-e126c98070ac)
![image](https://github.com/user-attachments/assets/377af6f0-7b9f-44c2-9ea4-4e9881d15d26)
![image](https://github.com/user-attachments/assets/8b636611-f9d2-4b25-9976-802569f917a7)
![image](https://github.com/user-attachments/assets/20e9698b-020d-434f-b6e6-c2a1401e15d1)
