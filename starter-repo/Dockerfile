FROM node:22-bookworm-slim AS frontend
WORKDIR /build/frontend
COPY starter-repo/frontend/package.json starter-repo/frontend/package-lock.json ./
RUN npm ci
COPY starter-repo/frontend/ ./
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8765 \
    HOST=0.0.0.0 \
    SCHEDULE_SOURCE_DIR=/app/data/training-ops
WORKDIR /app
COPY starter-repo/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home app
COPY starter-repo/codebase/ ./codebase/
COPY starter-repo/data/weekly-demo.json ./data/weekly-demo.json
COPY data/training-ops/teaching-schedule.xlsx data/training-ops/lab-coach-schedule.xlsx ./data/training-ops/
COPY --from=frontend /build/frontend/dist ./frontend/dist
RUN mkdir -p /app/.local && chown app:app /app/.local
USER app
EXPOSE 8765
CMD ["python", "codebase/web_app.py"]
