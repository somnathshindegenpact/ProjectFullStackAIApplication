FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "app:application", "--bind", "0.0.0.0:5000", "--workers", "3"]
