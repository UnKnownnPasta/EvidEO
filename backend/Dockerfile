FROM python:3.12-slim
WORKDIR /app
COPY backend/pyproject.toml backend/pyproject.toml
COPY backend/evideo backend/evideo
# Add ",ml" to EXTRAS for the optional RemoteCLIP land-cover instrument (pulls CPU torch, about 1 GB).
ARG EXTRAS=redis,geo
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu "./backend[${EXTRAS}]"
COPY config config
ENV EVIDEO_CONFIG=/app/config/evideo.yaml PYTHONUNBUFFERED=1
WORKDIR /app/backend
EXPOSE 8000
CMD ["uvicorn", "evideo.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
