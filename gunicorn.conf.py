"""Configuration file for Gunicorn."""

bind = "0.0.0.0:8000"
wsgi_app = "api.main:app"
worker_class = "uvicorn.workers.UvicornWorker"
workers = 4
max_requests = 2048
max_requests_jitter = 512
user = 61000
group = 61000
worker_temp_dir = "/dev/shm"
