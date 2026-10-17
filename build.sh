#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "=========================================="
echo "  NeuralPhish AI - Single-Service Build   "
echo "=========================================="

echo "[1/3] Upgrading pip and installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "[2/3] Installing frontend dependencies..."
cd frontend
npm install

echo "[3/3] Building frontend for production..."
npm run build
cd ..

echo "Build completed successfully! Frontend artifacts ready in frontend/dist."
