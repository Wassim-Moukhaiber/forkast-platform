FROM python:3.12-slim

LABEL maintainer="Forkast Platform"
LABEL description="Forkast - AI Restaurant Platform for MENA"

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make startup script executable
RUN chmod +x start.sh

# Expose ports: Streamlit (8517) and FastAPI (8518)
EXPOSE 8517 8518

# Health check against FastAPI
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
    CMD python -c "import httpx; httpx.get('http://localhost:8518/api/v1/health', timeout=3)" || exit 1

CMD ["./start.sh"]
