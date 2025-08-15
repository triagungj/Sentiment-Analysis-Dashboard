# Dockerfile for Django project
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirement.txt /app/
RUN pip install --upgrade pip && pip install -r requirement.txt

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Gunicorn for production
CMD ["gunicorn", "sentiment_dashboard.wsgi:application", "--bind", "0.0.0.0:8000", "--forwarded-allow-ips=*"]
