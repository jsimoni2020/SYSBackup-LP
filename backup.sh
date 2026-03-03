#!/bin/bash

SOURCE="/Users/justin.simoni/Downloads/"
DEST="/Volumes/2TB WorkDrive/Backup/"
LOG="/Users/justin.simoni/Projects/Backup/backup.log"

echo "========================================" >> "$LOG"
echo "Backup started: $(date)" >> "$LOG"

# Check that the 2TB drive is mounted
if [ ! -d "$DEST" ]; then
    mkdir -p "$DEST"
    if [ $? -ne 0 ]; then
        echo "ERROR: Cannot access destination: $DEST" >> "$LOG"
        echo "Is the 2TB WorkDrive connected?" >> "$LOG"
        exit 1
    fi
fi

# Copy all files from Downloads to Backup, overwriting existing files
rsync -av --progress "$SOURCE" "$DEST" >> "$LOG" 2>&1

echo "Backup completed: $(date)" >> "$LOG"
echo "========================================" >> "$LOG"
