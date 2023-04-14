# Prompt Counter for GPT-4

This tool helps you **monitor the number of prompts** sent to GPT-4, considering the prompt cap limitations. It records messages from the clipboard and updates a JSON file with the remaining tokens and reset time.

*Notes:*
- *GPT-4 currently has a cap of 25 messages every 3 hours.*  
*If it changes, you can edit it in the JSON file.*
- *I use the terms 'tokens' and 'prompts' interchangeably*
## Features

- Displays remaining tokens, current time, and reset time
- Automatically resets after cap hour interval
- Save message from the clipboard
- Open the message data folder
- Can reset time and tokens

## Usage

1. Run *PromptCounterGPT4.py* from the <a href="https://github.com/GokaGokai/promptCounterGPT4/releases">latest release</a>
2. Press `ctrl+b` to save message.
3. Press `ctrl+alt+o` to open the message data folder containing the JSON file.
4. Press `ctrl+alt+t` reset time and tokens on the next save.
5. Press `esc` to exit the script.

Upon opening example:
```
You have 24/25 tokens. (Reset time: 03:09)

Press 'ctrl+b'       to save message.
Press 'ctrl+alt+o'   to open message data dir.
Press 'ctrl+alt+t'   to reset time and tokens on the next save.
Press 'esc'          to exit.
```

Upon saving the message on highlighted text example:
```
Tokens left:    23
Current time:   00:11
Reset time:     03:09
Content:        Hey GPT4, what's 1+1?
```

## Dependencies

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

