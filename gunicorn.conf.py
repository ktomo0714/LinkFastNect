# Gunicorn configuration for Azure App Service
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "pos-api"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
keyfile = None
certfile = None

# Environment variables
raw_env = [
    f"DB_USER={os.getenv('DB_USER', '')}",
    f"DB_PASSWORD={os.getenv('DB_PASSWORD', '')}",
    f"DB_HOST={os.getenv('DB_HOST', '')}",
    f"DB_PORT={os.getenv('DB_PORT', '3306')}",
    f"DB_NAME={os.getenv('DB_NAME', '')}",
]
