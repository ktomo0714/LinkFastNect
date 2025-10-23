#!/bin/bash
# Azure App Service build script

echo "Running build script..."

# Python仮想環境の作成
if [ ! -d "antenv" ]; then
    echo "Creating virtual environment..."
    python -m venv antenv
fi

# 仮想環境の有効化
echo "Activating virtual environment..."
source antenv/bin/activate

# 依存関係のインストール
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"
