FROM node:22-bookworm-slim AS frontend
WORKDIR /build/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8765
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home app
COPY codebase/ ./codebase/
COPY data/weekly-demo.json ./data/weekly-demo.json
COPY --from=frontend /build/frontend/dist ./frontend/dist
USER app
EXPOSE 8765
CMD ["python", "codebase/web_app.py"]
