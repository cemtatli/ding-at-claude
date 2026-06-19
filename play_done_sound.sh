#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# By default, play the single ding sound. You can change this to clean_ding_3.opus
SOUND_FILE="$SCRIPT_DIR/clean_ding_3.opus"

if [ -f "$SOUND_FILE" ]; then
    # -nodisp: Don't show video window
    # -autoexit: Exit when finished playing
    # -loglevel quiet: Suppress ffmpeg output
    ffplay -nodisp -autoexit -loglevel quiet "$SOUND_FILE" >/dev/null 2>&1
else
    echo "Sound file not found: $SOUND_FILE"
fi
