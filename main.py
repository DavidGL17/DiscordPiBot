import feedparser
import time
import json
import os
import discord
from discord.ext import tasks
from settingsModule import Settings
from entry import Entry, entryFromFeedparserEntry


# Import settings and token from config files
settings = Settings()


##
## Setup functions
##

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




@tasks.loop(seconds=settings._settings['DEFAULT_WAIT_TIME'])
async def feedWatcher():
    # Read the control list
    with open(settings._settings['CONTROL_FILE'], "r") as controlFile:
        control = json.load(controlFile)
    # Fetch the feed again, and again, and again...
    f = feedparser.parse(settings._settings['FEED_URL'], agent=settings._settings['USER_AGENT'])

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to new control list.
    newControl = []
    newItems = 0
    await client.get_channel(settings._settings['CHANNEL_ID']).send("Checking feed...")
    for entries in f.entries:
        newControl.append(entries.id)
        if entries.id not in control:
            message = formatMessage(entries)

            await client.get_channel(settings._settings['CHANNEL_ID']).send(message)

            # Add entry guid to the control variable
            newItems += 1
        else:
            control.remove(entries.id)

    # TODO add a logging of items that are not in the feed anymore

    # Write the new control list to the control file
    with open(settings._settings['CONTROL_FILE'], "w") as controlFile:
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
if not os.path.isfile(settings._settings['CONTROL_FILE']):
    print("Doing initial setup...")
    # Set control to blank list
    control = []

    # Fetch the feed
    f = feedparser.parse(settings._settings['FEED_URL'], agent=settings._settings['USER_AGENT'])

    # If there are entries in the feed, add entry guid to the control variable
    if f.entries:
        for entries in f.entries:
            print(entries)
            exit(0)
            entry = entryFromFeedparserEntry(entries)
            control.append(entries.id)

    # Write the list to a json file for later use
    with open(settings._settings['CONTROL_FILE'], "w") as outfile:
        json.dump(control, outfile)

    # Only wait 30 seconds after initial run.
    time.sleep(settings._settings['INITIAL_WAIT_TIME'])

client.run(settings._settings['TOKEN'])
