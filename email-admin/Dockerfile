FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt requirements.txt

RUN apk update &&\
    apk add bash gcc build-base libffi-dev openssl-dev python3-dev zlib-dev &&\
    pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

COPY .. .

CMD ["gunicorn", "app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
