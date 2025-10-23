# Gunicorn configuration for Azure App Service
import multiprocessing
import os

# Server socket
port = int(os.getenv('WEBSITES_PORT', '8000'))
bind = f"0.0.0.0:{port}"
backlog = 2048

# Worker processes (Azure App Service用に調整)
workers = min(multiprocessing.cpu_count(), 2)  # Azure App Service用に制限
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 300  # Azure App Service用に延長
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

# Preload application for better performance
preload_app = True

# Environment variables
raw_env = [
    f"DB_USER={os.getenv('DB_USER', '')}",
    f"DB_PASSWORD={os.getenv('DB_PASSWORD', '')}",
    f"DB_HOST={os.getenv('DB_HOST', '')}",
    f"DB_PORT={os.getenv('DB_PORT', '3306')}",
    f"DB_NAME={os.getenv('DB_NAME', '')}",
    f"WEBSITES_PORT={port}",
]
