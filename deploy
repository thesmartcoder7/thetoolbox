#!/bin/bash

echo "Pulling latest code..."
git pull origin main

echo "Building frontend..."
cd frontend
npm install
npm run build --prod
cd ..

echo "Building backend..."
cd backend
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --noinput
cd ..

echo "Restarting Docker containers..."
docker-compose up --build -d
