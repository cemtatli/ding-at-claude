# Fall back to the copies bundled in the repo
[ -f "$SOUND_FILE" ] || SOUND_FILE="$SCRIPT_DIR/sounds/$SOUND_NAME"
[ -f "$SOUND_FILE" ] || SOUND_FILE="$SCRIPT_DIR/$SOUND_NAME"#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Sounds live outside the repo so git operations can't delete them.
# Pick any file from $SOUND_DIR (run generate_sounds.py to create more).
SOUND_DIR="${CLAUDE_SOUND_DIR:-$HOME/.claude/sounds}"
SOUND_NAME="question_pop.opus"

SOUND_FILE="$SOUND_DIR/$SOUND_NAME"
# Fall back to the copies bundled in the repo
[ -f "$SOUND_FILE" ] || SOUND_FILE="$SCRIPT_DIR/sounds/$SOUND_NAME"
[ -f "$SOUND_FILE" ] || SOUND_FILE="$SCRIPT_DIR/$SOUND_NAME"

if [ -f "$SOUND_FILE" ]; then
    # -nodisp: Don't show video window
    # -autoexit: Exit when finished playing
    # -loglevel quiet: Suppress ffmpeg output
    ffplay -nodisp -autoexit -loglevel quiet "$SOUND_FILE" >/dev/null 2>&1
else
    echo "Sound file not found: $SOUND_FILE"
fi
