#!/usr/bin/env bash
# Forkast Platform - Start both services
set -e

echo "Starting Forkast Platform..."

# Start FastAPI in background
echo "Starting FastAPI on port ${FORKAST_API_PORT:-8518}..."
python -m uvicorn api.main:app \
    --host 0.0.0.0 \
    --port "${FORKAST_API_PORT:-8518}" &

# Start Streamlit
echo "Starting Streamlit on port ${FORKAST_STREAMLIT_PORT:-8517}..."
python -m streamlit run web/app.py \
    --server.port "${FORKAST_STREAMLIT_PORT:-8517}" \
    --server.headless true \
    --server.address 0.0.0.0 \
    --server.enableCORS false \
    --server.enableXsrfProtection false

# If streamlit exits, stop everything
wait
