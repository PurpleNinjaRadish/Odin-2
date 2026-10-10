# Project Cerberus · Odin demo server (invented students only)
FROM python:3.12-slim
WORKDIR /app
COPY server.py ./
COPY public ./public
COPY db/schema.sql db/seed.sql ./db/
ENV HOST=0.0.0.0 \
    PORT=8080 \
    ODIN_DB=/app/data/odin_demo.db \
    PYTHONUNBUFFERED=1
RUN useradd --create-home odin && mkdir -p /app/data && chown odin /app/data
USER odin
VOLUME ["/app/data"]
EXPOSE 8080
CMD ["python", "server.py"]
