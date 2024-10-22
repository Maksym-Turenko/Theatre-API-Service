FROM python:3.12.3-alpine
LABEL maintainer="turenkomaksim099@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser -D -H my_user

USER my_user