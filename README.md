# Sentiment Analysis Dashboard

A Django-based dashboard for sentiment analysis of stock market and financial news.  
It provides both a **web interface** for visualization and a **REST API** for programmatic sentiment prediction.

---

## 🚀 Features

- 📊 Interactive dashboard to visualize sentiment trends
- 🤖 Sentiment prediction using **IndoBERT / IndoNLU** models
- 🔗 REST API for external integration
- 📰 News ingestion from CNBC Indonesia (RSS Feed)
- ⚙️ Admin dashboard for managing data and models
- 🐳 Easy deployment with **Docker & Docker Compose**

---

## 🗂️ Project Structure

```
.
├── api/                   # Django app for API endpoints
├── sentiment_dashboard/    # Main Django project (settings, URLs, WSGI)
├── model/                 # Pre-trained model files & configs
├── staticfiles/           # Static assets (CSS, JS, images)
├── templates/             # HTML templates for dashboard
├── docker-compose.yml     # Multi-container setup (web + db + worker)
└── requirements.txt       # Python dependencies
```

---

## ⚡ Getting Started (Local Development)

### 1. Clone Repository

```bash
git clone https://github.com/triagungj/Sentiment-Analysis-Dashboard.git
cd Sentiment-Analysis-Dashboard
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # on Linux/Mac
venv\Scripts\activate      # on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Access the dashboard at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🐳 Running with Docker

### 1. Build and Start Services

```bash
docker-compose up --build
```

This will start:

- `web`: Django app (running on port **8000**)
- `db`: PostgreSQL database
- `scheduler`: background service for fetching & analyzing news

### 2. Access the App

- Dashboard: [http://localhost:8000](http://localhost:8000)
- API Docs (Swagger): [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### 3. Common Commands

Run migrations:

```bash
docker-compose run web python manage.py migrate
```

Create superuser:

```bash
docker-compose run web python manage.py createsuperuser
```

Stop containers:

```bash
docker-compose down
```

---

## 📡 API Usage Example

**POST /api/predict/**

```json
{
  "text": "Harga saham BCA naik signifikan hari ini"
}
```

**Response:**

```json
{
  "label": "positive",
  "confidence": 0.94
}
```
