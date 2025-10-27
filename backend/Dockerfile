# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies including netcat
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install Python dependencies
COPY requirements*.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create staticfiles directory and set permissions
RUN mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app

# Collect static files as root user
RUN python manage.py collectstatic --noinput

# Add entrypoint script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
