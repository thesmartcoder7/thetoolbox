#!/bin/bash

# Function to run the frontend
start_frontend() {
  echo "Starting the frontend..."

  # Navigate to the frontend directory
  cd frontend || exit

  # Install npm dependencies
  npm install || { echo "Frontend installation failed!"; exit 1; }

  # Run the frontend (ng serve) in the background and redirect logs to a file
  nohup ng serve --host 0.0.0.0 --port 4200 > frontend.log 2>&1 &

  echo "Frontend started on http://localhost:4200"
}

# Function to run the backend
start_backend() {
  echo "Starting the backend..."

  # Navigate to the backend directory
  cd ../backend || exit

  # Set up the virtual environment
  source .venv/bin/activate || { echo "Backend virtual environment activation failed!"; exit 1; }

  # Install Python dependencies
  pip install -r requirements.txt || { echo "Backend installation failed!"; exit 1; }

  # Run the backend (Django server)
  python3 manage.py runserver 0.0.0.0:8000 || { echo "Backend server failed to start!"; exit 1; }
}

# Start the frontend
start_frontend

# Wait for frontend to fully initialize (you can adjust the time if necessary)
echo "Waiting for frontend to initialize..."
sleep 10 # Wait 10 seconds to give the frontend time to start

# Start the backend
start_backend
