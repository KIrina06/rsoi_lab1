FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

# Команда для Render: запуск через gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]