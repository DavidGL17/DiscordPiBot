import feedparser
import time
import json
import os
import discord
from discord.ext import tasks
from discordpibot.settingsModule import Settings
from discordpibot.entry import Entry, field_names, EntryEncoder


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

def prepareMessage(added_products, removed_products, current_products):
    # Send one big message with all the new products, removed products, and current products, as a sort of update on the current state of the feed.
    # If there is nothing to report, return a string that indicates that
    if not added_products and not removed_products and not current_products:
        return f"No changes to report.\n Next update at {time.strftime('%H:%M:%S', time.localtime(time.time() + settings._settings['DEFAULT_WAIT_TIME']))}"
    message = "Scanning the feed for updates, here is the current state:\n"
    if added_products:
        message += "New entries:\n"
        for product in added_products.values():
            message += f"{product.title}\n{product.link}\n"
    if removed_products:
        message += "Removed entries:\n"
        for product in removed_products.values():
            message += f"{product.title}\n{product.link}\n"
    if current_products:
        message += "Entries still active :\n"
        for product in current_products.values():
            message += f"{product.title}\n{product.link}\n"
    # add next update time (not in seconds but the actual time)
    message += f"Next update at {time.strftime('%H:%M:%S', time.localtime(time.time() + settings._settings['DEFAULT_WAIT_TIME']))}"
    return message



@tasks.loop(seconds=settings._settings['DEFAULT_WAIT_TIME'])
async def feedWatcher():
    print("Starting feed check...")
    # Read the control list
    with open(settings._settings['CONTROL_FILE'], "r") as controlFile:
        json_data = json.load(controlFile)
        prev_products = {k: Entry(**json_data[k]) for k in json_data}

    # Fetch the feed again, and again, and again...
    f = feedparser.parse(settings._settings['FEED_URL'], agent=settings._settings['USER_AGENT'])

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to new control list.
    # TODO remove this line once code is working
    await client.get_channel(settings._settings['CHANNEL_ID']).send("Checking feed...")

    current_products = {}
    # Convert the JSON array to a list of Product objects
    new_products = [Entry(**{name: p.get(name) for name in field_names}) for p in f.entries]
    # Create a dictionary of the new products
    for product in new_products:
        current_products[product.id] = product
    added_products = {k: v for k, v in current_products.items() if k not in prev_products}
    removed_products = {k: v for k, v in prev_products.items() if k not in current_products}
    message = prepareMessage(added_products, removed_products, current_products)
    if message:
        await client.get_channel(settings._settings['CHANNEL_ID']).send(message)
    prev_products = current_products

    # Write the new control list to the control file
    with open(settings._settings['CONTROL_FILE'], "w") as controlFile:
        json.dump(prev_products, controlFile, indent=4, cls=EntryEncoder)
    print(f"Checking done! warned for {len(added_products)} new items, and {len(removed_products)} removed items.")
    print(f"Next check at {time.strftime('%H:%M:%S', time.localtime(time.time() + settings._settings['DEFAULT_WAIT_TIME']))}")


# Activate the discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    # Start the feed watcher
    feedWatcher.start()


# Main program
def main():
    # Setup the control list if it does not exist
    if not os.path.isfile(settings._settings['CONTROL_FILE']):
        print("Doing initial setup...")
        # Set control to blank list
        control = {}

        # Write the list to a json file for later use
        with open(settings._settings['CONTROL_FILE'], "w") as outfile:
            json.dump(control, outfile)

        # Only wait 30 seconds after initial run.
        time.sleep(settings._settings['INITIAL_WAIT_TIME'])

    print("Starting feed check App...")
    client.run(settings._settings['TOKEN'])

if __name__ == "__main__":
    main()