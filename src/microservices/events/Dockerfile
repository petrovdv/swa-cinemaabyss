FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8082

CMD ["gunicorn", "--bind", "0.0.0.0:8082", "app:app"]
