#!/bin/bash
# Azure App Service startup script with virtual environment

echo "=== Azure App Service Startup ==="
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"

# 仮想環境のパスを設定
VENV_PATH="/home/site/wwwroot/antenv"

# 仮想環境の存在確認
if [ -d "$VENV_PATH" ]; then
    echo "Virtual environment found at: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "Virtual environment activated"
else
    echo "WARNING: Virtual environment not found, creating..."
    python -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 環境変数の確認
echo "=== Environment Variables ==="
echo "DB_USER: ${DB_USER:-Not set}"
echo "DB_HOST: ${DB_HOST:-Not set}"
echo "DB_NAME: ${DB_NAME:-Not set}"
echo "WEBSITES_PORT: ${WEBSITES_PORT:-8000}"
echo "============================="

# Pythonモジュールの確認
echo "Checking Python modules..."
python -c "import uvicorn; print(f'Uvicorn version: {uvicorn.__version__}')" || echo "ERROR: Uvicorn not installed"
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')" || echo "ERROR: FastAPI not installed"

# ポート設定
PORT=${WEBSITES_PORT:-8000}

# アプリケーションを起動
echo "Starting application on port ${PORT}..."
exec python -m uvicorn app:app --host 0.0.0.0 --port $PORT --log-level info
