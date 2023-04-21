FROM python:3.9

ADD . /app

EXPOSE 8080

WORKDIR /app/app

RUN pip install --upgrade pip && pip install -r requirements.txt
