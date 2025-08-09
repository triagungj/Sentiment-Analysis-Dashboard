# Sentiment Analysis Dashboard

This project is a Django-based dashboard for sentiment analysis, providing an API and web interface to analyze and visualize sentiment from various news sources.

## Features

- Sentiment analysis using a pre-trained model
- REST API for predictions
- Admin dashboard for managing data
- Static files for UI customization

## Project Structure

- `api/` – Django app for API endpoints and business logic
- `model/` – Pre-trained model files and configuration
- `sentiment_dashboard/` – Main Django project settings and URLs
- `staticfiles/` – Static assets (CSS, JS, images)

## Setup

1. Clone the repository:
   ```zsh
   git clone <your-repo-url>
   cd dashboard
   ```
2. Create and activate a Python virtual environment:
   ```zsh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```zsh
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```zsh
   python manage.py migrate
   ```
5. Run the development server:
   ```zsh
   python manage.py runserver
   ```

## Usage

- Access the dashboard at `http://127.0.0.1:8000/`
- Use the API endpoints for sentiment predictions

## License

This project is licensed under the MIT License.
