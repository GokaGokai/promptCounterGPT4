"""
Author: GokaGokai
Version: 1.1.0
Description: A script to keep track of the number of prompts sent to GPT-4 due to the prompt cap.
"""

import json
from datetime import datetime, timedelta
import keyboard
import win32clipboard
import os

MAXTOKEN = 25
APP_NAME = "PromptCounterGPT4"
DATA_DIR = os.path.join(os.getenv("LOCALAPPDATA"), APP_NAME)
JSON_FILE = os.path.join(DATA_DIR, "message_data.json")

def get_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


def write_to_file(data):
    if not os.path.isfile(JSON_FILE):
        print("No message data found. A new file has been created.\n")

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        with open(JSON_FILE, "w") as f:
            json.dump({"messages": []}, f, indent=4)

    with open(JSON_FILE, "r+") as f:
        global resetTimeAndTokensBool
        message_data = json.load(f)

        # calculate token_left and reset_time based on previous messages
        current_time = datetime.now()
        latest_message = message_data["messages"][-1] if message_data["messages"] else None
        if (latest_message and current_time - datetime.strptime(latest_message["reset_time"], '%Y-%m-%d %H:%M:%S.%f') > timedelta(hours=3)) or resetTimeAndTokensBool:
            token_left = MAXTOKEN - 1
            reset_time = datetime.now() + timedelta(hours=3)
            resetTimeAndTokensBool = False
        elif latest_message is None:
            token_left = MAXTOKEN - 1
            reset_time = latest_message["reset_time"] if latest_message else datetime.now() + timedelta(hours=3)
        else:
            token_left = latest_message["token_left"] - 1 if latest_message and latest_message["token_left"] > 0 else 0
            reset_time = latest_message["reset_time"] if latest_message else datetime.now() + timedelta(hours=3)

        # add new message to the message_data
        new_message = {
            "timestamp": str(datetime.now()),
            "reset_time": str(reset_time),
            "token_left": token_left,
            "content": data
        }
        message_data["messages"].append(new_message)

        # write the updated data to the file
        f.seek(0)
        json.dump(message_data, f, indent=4)
        f.truncate()

        # print current status
        print(f"Tokens left:    {token_left}")
        print(f"Current time:   {datetime.now().strftime('%H:%M')}")
        print(f"Reset time:     {datetime.strptime(str(reset_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M')}")
        print(f"Content:        {data}\n")

def read_from_file():
    if not os.path.isfile(JSON_FILE):
        print("No message data found.")
        return

    os.startfile(DATA_DIR)

def resetTimeAndTokens():
    global resetTimeAndTokensBool
    resetTimeAndTokensBool = True
    print("Reset time and tokens")
    print(f"You have {MAXTOKEN}/{MAXTOKEN} tokens.\n")

def main():
    global resetTimeAndTokensBool
    resetTimeAndTokensBool = False

    if not os.path.isfile(JSON_FILE):
        print("No message data found. A new file has been created.")
        print(f"You have {MAXTOKEN}/{MAXTOKEN} tokens.\n")

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        with open(JSON_FILE, "w") as f:
            json.dump({"messages": []}, f, indent=4)
    else:
        with open(JSON_FILE, "r+") as f:
            message_data = json.load(f)
            latest_message = message_data["messages"][-1] if message_data["messages"] else None
            if latest_message is not None:
                token_left = latest_message["token_left"]
                reset_time = latest_message["reset_time"]
                print(f"You have {token_left}/{MAXTOKEN} tokens. (Reset time: {datetime.strptime(str(reset_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M')}) \n")
            else:
                print(f"You have {MAXTOKEN}/{MAXTOKEN} tokens.\n")

    keyboard.add_hotkey("ctrl+b", lambda: write_to_file(get_clipboard()))
    keyboard.add_hotkey("ctrl+alt+o", read_from_file)
    keyboard.add_hotkey("ctrl+alt+t", resetTimeAndTokens)
    print("Press 'ctrl+b' to record clipboard data.")
    print("Press 'ctrl+alt+o' to open message data.")
    print("Press 'ctrl+alt+t' to reset time and tokens.")
    print("Press 'esc' to exit.\n")
    while True:
        if keyboard.is_pressed("esc"):
            break

if __name__ == "__main__":
    main()
