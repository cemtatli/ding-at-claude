# 🔔 Claude Code Sound Notifications

Bring your Claude Code CLI to life with audible feedback! This project provides simple scripts and configuration to play a notification "ding" when Claude finishes a task or asks for your input.

## Features
- **Task Completed Notification:** Hear a sound when Claude finishes processing.
- **Input Needed Notification:** Hear a sound when Claude is waiting for your response or question.
- **Audio Processing:** Includes a python script to clean up any raw audio if you want to use custom sounds.

## Prerequisites

To play the sounds, you must have `ffplay` installed:

```bash
# On Debian/Ubuntu
sudo apt install ffmpeg

# On macOS
brew install ffmpeg
```

## Global Configuration (Recommended)

You can configure Claude Code to use these notifications for all your projects by adding `hooks` to your global Claude config file (`~/.claude/settings.json`).

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /absolute/path/to/ding-at-claude/play_done_sound.sh",
            "statusMessage": "Playing done sound..."
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "bash /absolute/path/to/ding-at-claude/play_question_sound.sh",
            "statusMessage": "Playing question sound..."
          }
        ]
      }
    ]
  }
}
```
*(Remember to replace `/absolute/path/to/ding-at-claude` with the actual path where you cloned this repository!)*

## Local Configuration

If you only want this active in a specific project, create a `.claude/settings.local.json` inside that project's folder with the exact same JSON configuration shown above.
