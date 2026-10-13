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

## Choosing a Sound

Synthesized sounds ship in `sounds/` (`done_bell`, `done_marimba`, `done_glass_chord`, `done_kalimba`, `done_soft`, `question_bell`, `question_marimba`, `question_pop`, `question_glass`, `question_kalimba`), alongside the original `clean_ding_3.opus` / `clean_ding_tek.opus`.

Set `SOUND_NAME` in `play_done_sound.sh` / `play_question_sound.sh` to pick one. Scripts look in `~/.claude/sounds/` first (override with `CLAUDE_SOUND_DIR`), then fall back to the copies in this repo, so your sounds survive git operations on the repo.

Preview all of them:

```bash
for f in sounds/*.opus; do echo "$f"; ffplay -nodisp -autoexit -loglevel quiet "$f"; done
```

Generate them again (or tweak and make your own) into `~/.claude/sounds/`:

```bash
uv run generate_sounds.py   # or: python3 generate_sounds.py (needs numpy)
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
