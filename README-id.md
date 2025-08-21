# Sentiment Analysis Dashboard

Dashboard **Django** untuk analisis sentimen berita saham/keuangan.  
Menyediakan antarmuka web untuk visualisasi serta endpoint API untuk prediksi sentimen.

---

## 0) Persiapan Lingkungan (Env & Prasyarat)

**Prasyarat umum**
- Git
- Python ≥ 3.10 (hanya diperlukan untuk jalankan tanpa Docker)
- PostgreSQL ≥ 14 (hanya diperlukan untuk jalankan tanpa Docker)
- Docker Desktop / Docker Engine + Docker Compose (opsional, jika memilih jalankan dengan Docker)

**Kloning repositori**
```bash
git clone https://github.com/triagungj/Sentiment-Analysis-Dashboard.git
cd Sentiment-Analysis-Dashboard
```

**Buat berkas `.env`** (berlaku untuk kedua opsi)
Salin dari `.env.example` bila tersedia atau buat baru. Nilai di bawah ini adalah contoh minimal.
```env
# Django
DJANGO_SECRET_KEY=ubah-ke-random-string
DEBUG=1
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL
POSTGRES_DB=sentiment_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Catatan:
# - Jika pakai Docker, biarkan HOST= db (mengikuti service name di docker compose)
# - Jika tanpa Docker, set HOST=127.0.0.1
POSTGRES_HOST=db
POSTGRES_PORT=5432

# (Opsional) Jika project-mu mendukung DATABASE_URL, kamu bisa pakai baris ini sebagai pengganti variabel di atas:
# DATABASE_URL=postgresql://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/POSTGRES_DB
```

> **Tips**: Simpan `.env` di root project yang sama dengan `manage.py` agar bisa dibaca oleh konfigurasi Django.

---

## Opsi 1 — Menjalankan dengan Docker (Direkomendasikan)

1) **Jalankan layanan**
```bash
# Compose v2 (direkomendasikan)
docker compose up --build -d

# atau (Compose v1)
# docker-compose up --build -d
```

2) **Migrasi database & buat superuser (di dalam container)**
```bash
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

3) **Akses aplikasi**
- Dashboard: http://localhost:8000

4) **Perintah umum Docker**
```bash
# Melihat status & log
docker compose ps
docker compose logs -f web
docker compose logs -f db

# Hentikan layanan
docker compose down

# Hapus semua volume (termasuk data database) — gunakan dengan hati‑hati
docker compose down -v
```

---

## Opsi 2 — Menjalankan Tanpa Docker (Lokal)

1) **Instal PostgreSQL** (pastikan `psql` tersedia).  
   Buat **database** dan **user**:
```sql
-- Masuk sebagai superuser (misal: postgres) lalu jalankan:
CREATE DATABASE sentiment_db;
CREATE USER sentiment_user WITH PASSWORD 'ganti-password';
ALTER ROLE sentiment_user SET client_encoding TO 'utf8';
ALTER ROLE sentiment_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sentiment_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sentiment_db TO sentiment_user;
```

2) **Perbarui `.env` untuk koneksi lokal**
```env
POSTGRES_DB=sentiment_db
POSTGRES_USER=sentiment_user
POSTGRES_PASSWORD=ganti-password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

3) **Buat virtualenv & instal dependensi Python**
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instal dependencies (pakai nama file yang sesuai, mis. requirements.txt)
pip install -r requirements.txt
# jika repositori menggunakan requirement.txt:
# pip install -r requirement.txt
```

4) **Migrasi & jalankan server pengembangan**
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Akses di: http://127.0.0.1:8000

---

## Perintah Berguna (Keduanya)

```bash
# Cek konfigurasi Django
python manage.py check

# Masuk shell database dari Django (butuh psql di PATH)
python manage.py dbshell

# Kumpulkan static (untuk deployment)
python manage.py collectstatic
```

---

## Backup & Restore Database

**Dengan Docker**
```bash
# Backup
docker exec -t $(docker ps -qf "name=_db") pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" > backup.sql

# Restore
cat backup.sql | docker exec -i $(docker ps -qf "name=_db") psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
```

**Tanpa Docker (lokal)**
```bash
# Backup
pg_dump -U sentiment_user -d sentiment_db > backup.sql

# Restore
psql -U sentiment_user -d sentiment_db -f backup.sql
```

---

## Troubleshooting

- **`OperationalError: could not connect to server`**  
  Pastikan layanan Postgres aktif. Jika Docker, cek `docker compose logs -f db` dan pastikan `POSTGRES_HOST=db`.

- **`FATAL: password authentication failed for user ...`**  
  Pastikan username/password di `.env` sesuai dengan user yang dibuat di Postgres/Compose.

- **Perubahan model tidak terdeteksi**  
  Jalankan `python manage.py makemigrations` lalu `python manage.py migrate`.

- **Port 8000 sudah digunakan**  
  Matikan proses lain yang memakai port 8000 atau jalankan `python manage.py runserver 0.0.0.0:8001` (ubah port sesuai kebutuhan).

---

## Struktur Proyek (Ringkas)

```
.
├── api/                    # Endpoint API
├── sentiment_dashboard/    # Settings/URL/Wsgi Django
├── templates/              # HTML templates
├── staticfiles/            # Static assets
├── docker-compose.yml      # web + db (+ scheduler jika ada)
├── Dockerfile
├── .env.example            # Contoh env (opsional)
├── manage.py
├── requirements.txt / requirement.txt
└── README.md
```

---

## Lisensi
Tentukan lisensi proyek (mis. MIT) dan tambahkan berkas `LICENSE` jika diperlukan.
