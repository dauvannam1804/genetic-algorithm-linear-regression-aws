#!/bin/bash

# This script automates the deployment of the Gradio application.

# Exit immediately if a command exits with a non-zero status.
set -e

# Define constants
APP_FILE="src/app.py"
APP_PATTERN="app.py"
MODEL_WEIGHTS_DIR="src/weights"
MODEL_WEIGHTS_FILE="$MODEL_WEIGHTS_DIR/genetic_lr_weights.npy"
FETCH_MODEL_SCRIPT="src/utils/fetch_model_s3.py" # Script to fetch the model

# --- 2. Fetch Latest Model from S3 ---
echo "
--- Fetching latest model from S3 ---"
# Ensure the weights directory exists
mkdir -p "$MODEL_WEIGHTS_DIR"


# Run the script to fetch the model
python "$FETCH_MODEL_SCRIPT"

# --- 3. Run the Application ---
echo "
--- Deploying Gradio Application ---"

# Find and kill the old running Gradio process
if pgrep -f "$APP_PATTERN" > /dev/null; then
    echo "Found old process. Killing it..."
    pkill -f "$APP_PATTERN"
    sleep 2 # Give it a moment to shut down
fi

# Start the Gradio app in the background
# Use nohup to keep it running after the shell exits
# Redirect stdout and stderr to a log file
echo "Starting Gradio server in background..."
nohup python "$APP_FILE" > gradio_app.log 2>&1 &

# Give it a moment to start up
sleep 5

# --- 4. Verify Deployment ---
echo "
--- Verifying Deployment ---"
# Check if the process is running
if pgrep -f "$APP_PATTERN" > /dev/null; then
    echo "✅ Deployment successful! Gradio app is running."
else
    echo "❌ Deployment failed. The Gradio app is not running."
    exit 1
fi

