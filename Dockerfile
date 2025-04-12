FROM python:3.7.8-slim

# OS 패키지 설치 (psycopg2-binary 설치에 필요)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

#CMD ["ddtrace-run", "python", "app.py"]

CMD ["python", "-u", "app.py"]
