# Sentiment Analysis Dashboard

A **Django** dashboard for sentiment analysis of stock/financial news.  
It provides a web UI for visualization and REST endpoints for programmatic predictions.

---

## 0) Environment Preparation (Env & Prerequisites)

**Prerequisites**
- Git
- Python ≥ 3.10 (only required if running *without* Docker)
- PostgreSQL ≥ 14 (only required if running *without* Docker)
- Docker Desktop / Docker Engine + Docker Compose (optional, if you choose the Docker path)

**Clone the repository**
```bash
git clone https://github.com/triagungj/Sentiment-Analysis-Dashboard.git
cd Sentiment-Analysis-Dashboard
```

**Create a `.env` file** (used by both options)  
Copy from `.env.example` if available, or create a new one. The following is a minimal example:
```env
# Django
DJANGO_SECRET_KEY=change-to-a-random-string
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL
POSTGRES_DB=sentiment_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Notes:
# - If you run with Docker, keep HOST= db (service name in docker compose)
# - If you run without Docker, set HOST=127.0.0.1
POSTGRES_HOST=db
POSTGRES_PORT=5432

# (Optional) If your project supports DATABASE_URL, you can use this instead:
# DATABASE_URL=postgresql://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/POSTGRES_DB
```

> **Tip**: Put `.env` in the project root (next to `manage.py`) so Django can load it.

---

## Option 1 — Run with Docker (Recommended)

1) **Start services**
```bash
# Compose v2 (recommended)
docker compose up --build -d

# or (Compose v1)
# docker-compose up --build -d
```

2) **Apply migrations & create a superuser (inside the container)**
```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

3) **Open the app**
- Dashboard: http://localhost:8000

4) **Common Docker commands**
```bash
# Check status & view logs
docker compose ps
docker compose logs -f web
docker compose logs -f db

# Stop services
docker compose down

# Remove volumes (including DB data) — be careful
docker compose down -v
```

---

## Option 2 — Run Locally (Without Docker)

1) **Install PostgreSQL** (ensure `psql` is available).  
   Create a **database** and **user**:
```sql
-- Log in as a superuser (e.g., postgres) then run:
CREATE DATABASE sentiment_db;
CREATE USER sentiment_user WITH PASSWORD 'change-password';
ALTER ROLE sentiment_user SET client_encoding TO 'utf8';
ALTER ROLE sentiment_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sentiment_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sentiment_db TO sentiment_user;
```

2) **Update `.env` for local connection**
```env
POSTGRES_DB=sentiment_db
POSTGRES_USER=sentiment_user
POSTGRES_PASSWORD=change-password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

3) **Create a virtualenv & install Python dependencies**
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies (use the file in your repo)
pip install -r requirement.txt
# if your repo uses requirement.txt:
# pip install -r requirement.txt
```

4) **Migrate & run the development server**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open: http://127.0.0.1:8000

---

## Useful Commands (Both Options)

```bash
# Validate Django project settings
python manage.py check

# Database shell from Django (requires `psql` in PATH)
python manage.py dbshell

# Collect static files (for production)
python manage.py collectstatic
```

---

## Database Backup & Restore

**With Docker**
```bash
# Backup
docker exec -t $(docker ps -qf "name=_db") pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > backup.sql

# Restore
cat backup.sql | docker exec -i $(docker ps -qf "name=_db") psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

**Without Docker (local)**
```bash
# Backup
pg_dump -U sentiment_user -d sentiment_db > backup.sql

# Restore
psql -U sentiment_user -d sentiment_db -f backup.sql
```

---

## Troubleshooting

- **`OperationalError: could not connect to server`**  
  Ensure PostgreSQL is running. With Docker, check `docker compose logs -f db` and confirm `POSTGRES_HOST=db`.

- **`FATAL: password authentication failed for user ...`**  
  Ensure the credentials in `.env` match the actual DB user.

- **Model changes not detected**  
  Run `python manage.py makemigrations` then `python manage.py migrate`.

- **Port 8000 already in use**  
  Stop the process using port 8000 or run `python manage.py runserver 0.0.0.0:8001` (change the port as needed).

---

## Project Structure (Brief)

```
.
├── api/                    # API endpoints
├── sentiment_dashboard/    # Django settings/urls/wsgi
├── templates/              # HTML templates
├── staticfiles/            # Static assets
├── docker-compose.yml      # web + db (+ optional scheduler)
├── Dockerfile
├── .env.example            # Example env (optional)
├── manage.py
├── requirement.txt / requirement.txt
└── README.md
```

---

## License
Choose a license (e.g., MIT) and add a `LICENSE` file if needed.
