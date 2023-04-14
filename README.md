# Prompt Counter for GPT-4

This script helps you monitor the number of prompts sent to GPT-4, considering the prompt cap limitations. It records messages from the clipboard and updates a JSON file with the remaining tokens and reset time.

## Features

- Records clipboard data with a hotkey
- Displays remaining tokens, current time, and reset time
- Opens the message data folder with a hotkey

## Usage

1. Run the script with Python.
2. Press `ctrl+b` to record the clipboard data as a prompt sent to GPT-4.
3. Press `ctrl+alt+p` to open the message data folder containing the JSON file.
4. Press `esc` to exit the script.

## Dependencies

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

