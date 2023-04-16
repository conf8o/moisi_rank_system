FROM python:3.9

COPY . /app

EXPOSE 8080

WORKDIR /app/app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
