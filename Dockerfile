# Python slim image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# System deps (optional; psycopg2-binary doesn't require build tools)
RUN apt-get update && apt-get install -y --no-install-recommends     netcat-traditional     && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . /app
# Collect static files (after copying project)
RUN python manage.py collectstatic --noinput

# Entrypoint waits for DB then runs migrations and launches gunicorn
ENTRYPOINT ["bash", "-lc", "echo 'Waiting for db...' && until nc -z $POSTGRES_HOST $POSTGRES_PORT; do sleep 1; done && python manage.py makemigrations && python manage.py migrate && gunicorn book_manager.wsgi:application --bind 0.0.0.0:8000"]
