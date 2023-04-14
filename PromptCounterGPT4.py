"""
Author: GokaGokai
Version: 1.2.0
Description: A script to keep track of the number of prompts sent to GPT-4 due to the prompt cap.
"""

import json
from datetime import datetime, timedelta
import keyboard
import win32clipboard
import os

APP_NAME = "PromptCounterGPT4"
DATA_DIR = os.path.join(os.getenv("LOCALAPPDATA"), APP_NAME)
JSON_FILE = os.path.join(DATA_DIR, "message_data.json")

# Default
maxtoken = 25
resetInterval = 3


# ------------------
# Internal functions
# ------------------   
def saveMessage(data):
    if not os.path.isfile(JSON_FILE):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        with open(JSON_FILE, "w") as f:
            json.dump({"maxtoken": 25, "resetInterval": 3, "messages": []}, f, indent=4)

        print("No message data found. A new file has been created.\n")

    with open(JSON_FILE, "r+") as f:
        global resetTimeAndTokensBool
        message_data = json.load(f)
        maxtoken = message_data["maxtoken"]
        resetInterval = message_data["resetInterval"]

        # calculate token_left and reset_time based on previous messages
        current_time = datetime.now()
        latest_message = message_data["messages"][-1] if message_data["messages"] else None
        if (latest_message and current_time - datetime.strptime(latest_message["reset_time"], '%Y-%m-%d %H:%M:%S.%f') > timedelta(hours=resetInterval)) or resetTimeAndTokensBool:
            token_left = maxtoken - 1
            reset_time = datetime.now() + timedelta(hours=resetInterval)
            resetTimeAndTokensBool = False
        elif latest_message is None:
            token_left = maxtoken - 1
            reset_time = latest_message["reset_time"] if latest_message else datetime.now() + timedelta(hours=resetInterval)
        else:
            token_left = latest_message["token_left"] - 1 if latest_message and latest_message["token_left"] > 0 else 0
            reset_time = latest_message["reset_time"] if latest_message else datetime.now() + timedelta(hours=resetInterval)

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

        printCurrentStatus(token_left,reset_time,data)

def openMessageDir():
    if not os.path.isfile(JSON_FILE):
        print("No message data found.")
        return
    os.startfile(DATA_DIR)

def resetTimeAndTokens():
    global resetTimeAndTokensBool
    resetTimeAndTokensBool = True
    resetString = "None"

    print("Reset time and tokens on the next save")
    print(f"You have {maxtoken}/{maxtoken} tokens. (Reset time: {resetString}) \n")

def getClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data


# ------
# Prints
# ------
def printShortcut():
    print("Press 'ctrl+b'       to save message.")
    print("Press 'ctrl+alt+o'   to open message data dir.")
    print("Press 'ctrl+alt+t'   to reset time and tokens on the next save.")
    print("Press 'esc'          to exit.\n")

def printCurrentStatus(token_left, reset_time, data):
    print(f"Tokens left:    {token_left}")
    print(f"Current time:   {datetime.now().strftime('%H:%M')}")
    print(f"Reset time:     {datetime.strptime(str(reset_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M')}")
    print(f"Content:        {data}\n")


# ------
# Main
# ------
def main():
    global maxtoken, resetInterval, resetTimeAndTokensBool
    resetTimeAndTokensBool = False

    if not os.path.isfile(JSON_FILE):
        resetString = "None"
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        with open(JSON_FILE, "w") as f:
            json.dump({"maxtoken": maxtoken, "resetInterval": resetInterval, "messages": []}, f, indent=4)

        print("No message data found. A new file has been created.")
        print(f"You have {maxtoken}/{maxtoken} tokens. (Reset time: {resetString}) \n")

    else:
        with open(JSON_FILE, "r+") as f:
            message_data = json.load(f)
            maxtoken = message_data["maxtoken"]
            resetInterval = message_data["resetInterval"]
            latest_message = message_data["messages"][-1] if message_data["messages"] else None
            current_time = datetime.now()
            resetString = ""
            if latest_message is not None:
                token_left = latest_message["token_left"]
                reset_time = latest_message["reset_time"]
                resetString = datetime.strptime(str(reset_time), '%Y-%m-%d %H:%M:%S.%f').strftime('%H:%M')
                if (latest_message and current_time - datetime.strptime(latest_message["reset_time"], '%Y-%m-%d %H:%M:%S.%f') > timedelta(hours=resetInterval)):
                    token_left = maxtoken
            else:
                token_left = maxtoken
                resetString = "None"

            print(f"You have {token_left}/{maxtoken} tokens. (Reset time: {resetString}) \n")

    keyboard.add_hotkey("ctrl+b", lambda: saveMessage(getClipboard()))
    keyboard.add_hotkey("ctrl+alt+o", openMessageDir)
    keyboard.add_hotkey("ctrl+alt+t", resetTimeAndTokens)

    printShortcut()

    while True:
        if keyboard.is_pressed("esc"):
            break

if __name__ == "__main__":
    main()
