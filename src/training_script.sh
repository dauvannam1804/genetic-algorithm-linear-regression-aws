#!/bin/bash

# This script automates the process of preparing data and training the model.

# Set script to exit immediately if a command exits with a non-zero status.
set -e

# Define paths
DATA_FILE="src/data/advertising.csv"
DATA_DIR="src/data"
FETCH_SCRIPT="src/utils/fetch_dataset_s3.py"
UPLOAD_SCRIPT="src/utils/upload_dataset_s3.py"
TRAIN_SCRIPT="src/model/train.py"

# 1. Check for local data file
if [ -f "$DATA_FILE" ]; then
    echo "✅ Data file found locally at $DATA_FILE."
else
    echo "⚠️ Data file not found at $DATA_FILE."
    echo "🔄 Attempting to fetch data from S3..."

    # Ensure the data directory exists
    mkdir -p "$DATA_DIR"

    # 2. Try to fetch from S3.
    if python "$FETCH_SCRIPT"; then
        echo "✅ Data successfully fetched from S3."
    else
        echo "⚠️ Could not fetch data from S3. It might not exist yet."
        echo "🚀 Uploading data from URL to S3..."

        # 3. Upload data to S3 from the source URL.
        python "$UPLOAD_SCRIPT"

        echo "🔄 Retrying fetch from S3 after upload..."
        # 4. Retry fetching from S3. If this fails, the script will exit due to `set -e`.
        python "$FETCH_SCRIPT"
    fi
    echo "✅ Data successfully prepared."
fi

# 5. Run the training script
python "$TRAIN_SCRIPT"

