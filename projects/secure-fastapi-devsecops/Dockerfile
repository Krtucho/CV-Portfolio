FROM python:3.12-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .
RUN pip install --no-cache-dir --prefix=/install .

FROM gcr.io/distroless/python3-debian12:nonroot

COPY --from=builder /install /usr/local
COPY --from=builder /build/app /app

USER nonroot:nonroot
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
