# SENTINEL core — modular monolith. Multi-stage; runs the embedded profile by default, or the
# production profile against the docker-compose store topology (PRAHARI_PROFILE=production).
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install -e ".[production]"

COPY app ./app
COPY prompts ./prompts

# Seed the embedded corpus at build time so the image is demo-ready out of the box.
RUN python -m app.seed || true

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
