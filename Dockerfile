FROM python:3.10.6-alpine3.16

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN apk add --no-cache git gcc musl-dev \
  mariadb-client mariadb-dev nodejs-current npm

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY package.json package-lock.json ./
RUN npm install

COPY . ./
EXPOSE 8000
