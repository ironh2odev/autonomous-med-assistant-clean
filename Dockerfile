FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential python3-dev git \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean

COPY . .

EXPOSE 8080

CMD ["python", "api.main"]