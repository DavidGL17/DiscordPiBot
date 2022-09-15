import feedparser
import time
import json
import os
import discord
from discord.ext import tasks

# Settings
INITIAL_WAIT_TIME = 30  # 30 seconds
DEFAULT_WAIT_TIME = 30  # 10 minutes
TOKEN_FILE_NAME = "token.txt"
CONTROL_FILE = "control.json"
MESSAGE_TITLE = "New Raspberry Pi found!"

# Feed URL
FEED_URL = "https://rpilocator.com/feed/?country=DE&cat=CM4,PI4,PIZERO"

# User Agent
USER_AGENT = "DiscordPi feed alert"
CHANNEL_ID = 1019198548149022720

# Create the message body
def formatMessage(entry, isNew=True):
    if isNew:
        message = f"Alert, new item available\n{entry.title}\n{entry.link}"
    else:
        message = (
            f"Alert, this item is no longer available\n{entry.title}\n{entry.link}"
        )
        pass

    return message


@tasks.loop(seconds=DEFAULT_WAIT_TIME)
async def feedWatcher():
    # Read the control list
    with open(CONTROL_FILE, "r") as controlFile:
        control = json.load(controlFile)
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to new control list.
    newControl = []
    newItems = 0
    await client.get_channel(CHANNEL_ID).send("Checking feed...")
    for entries in f.entries:
        newControl.append(entries.id)
        if entries.id not in control:
            message = formatMessage(entries)

            await client.get_channel(CHANNEL_ID).send(message)

            # Add entry guid to the control variable
            newItems += 1
        else:
            control.remove(entries.id)

    # TODO add a logging of items that are not in the feed anymore

    # Write the new control list to the control file
    with open(CONTROL_FILE, "w") as controlFile:
        json.dump(newControl, controlFile)
    print(f"Checking done! warned for {newItems} new items")


# Main program

# Activate the discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    # Start the feed watcher
    feedWatcher.start()


# Setup the control list if it does not exist
if not os.path.isfile(CONTROL_FILE):
    print("Doing initial setup...")
    # Set control to blank list
    control = []

    # Fetch the feed
    f = feedparser.parse(FEED_URL, agent=USER_AGENT)

    # If there are entries in the feed, add entry guid to the control variable
    if f.entries:
        for entries in f.entries:
            control.append(entries.id)

    # Write the list to a json file for later use
    with open(CONTROL_FILE, "w") as outfile:
        json.dump(control, outfile)

    # Only wait 30 seconds after initial run.
    time.sleep(INITIAL_WAIT_TIME)

# read the token from the file
TOKEN = open(TOKEN_FILE_NAME, "r").read()

client.run(TOKEN)
