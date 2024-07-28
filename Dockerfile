FROM python:slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:3000", "--worker-class", "aiohttp.GunicornWebWorker", "--workers=4"]

