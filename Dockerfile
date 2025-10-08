# ===== Stage 1: Build =====
FROM python:3.13-slim AS build

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip & dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt

# ===== Stage 2: Runtime =====
FROM python:3.13-slim

# Set Python environment variables again
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed packages from build stage
COPY --from=build /install /usr/local

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port for Gunicorn
EXPOSE 8000

# Use Gunicorn for production/dev
CMD ["gunicorn", "myportfolio.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
