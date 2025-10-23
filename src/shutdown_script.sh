#!/bin/bash

# This script stops the running Gradio application.

set -e

APP_PATTERN="app.py" # Use a more general pattern

echo "--- Shutting down Gradio Application ---"

# Find and kill the running application process by pattern.
if pgrep -f "$APP_PATTERN" > /dev/null; then
    echo "Found running process. Killing it..."
    pkill -f "$APP_PATTERN"
    echo "✅ Application shut down successfully."
else
    echo "⚠️ No running application found."
fi
