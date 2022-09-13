import requests
import feedparser
import time
import json
import os
import discord

# Settings
DEFAULT_WAIT_TIME = 600  # 10 minutes
TOKEN_FILE_NAME = "token.txt"
MESSAGE_TITLE = "New Raspberry Pi found!"

# Feed URL
FEED_URL = "https://rpilocator.com/feed/"

# User Agent
USER_AGENT = "DiscordPi feed alert"
CHANNEL_ID = 1019198548149022720

# Create the message body
def formatMessage(entry):
    message = {
        "title": MESSAGE_TITLE,
        "message": entry.title + ": " + entry.link,
        "extras": {"client::notification": {"click": {"url": entry.link}}},
    }

    message = json.dumps(message)

    return message


# Main program

# Activate the discord client
client = discord.Client()


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


# read the token from the file
TOKEN = open(TOKEN_FILE_NAME, "r").read()

client.run(TOKEN)


# Set control to blank list
control = []

# Fetch the feed
f = feedparser.parse(FEED_URL, agent=USER_AGENT)

# If there are entries in the feed, add entry guid to the control variable
if f.entries:
    for entries in f.entries:
        control.append(entries.id)

# Only wait 30 seconds after initial run.
time.sleep(30)

client.se

while True:
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to new control list.
    newControl = []
    for entries in f.entries:
        if entries.id not in control:

            message = formatMessage(entries)

            sendMessage(message)

            # Add entry guid to the control variable
            newControl.append(entries.id)
            control.remove(entries.id)

    # Replace old control with new one to update the currently available entries
    control = newControl

    time.sleep(DEFAULT_WAIT_TIME)
