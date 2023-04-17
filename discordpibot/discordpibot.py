import feedparser
import time
import asyncio
import json
import os
import discord
from .settingsModule import cron_string, control_file, feed_url, user_agent, channel_id, token, timezone
from .logging import logger
from .entry import Entry, field_names, EntryEncoder
from croniter import croniter
from datetime import datetime


##
# Setup functions
##


def prepareMessage(added_products: dict, removed_products: dict, current_products: dict, next_update: datetime) -> str:
    # Send one big message with all the new products, removed products, and current products, as a sort of update on the current state of the feed.
    # If there is nothing to report, return a string that indicates that

    if not added_products and not removed_products and not current_products:
        return f"There is nothing selling, and nothing was removed.\nNext update at {next_update.strftime('%H:%M %Z on the %d.%m')}"
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
    # print next update time, full (so day.month, hour:minute)
    message += f"Next update at {next_update.strftime('%H:%M %Z on the %d.%m')}"
    return message


async def feedWatcher(next_update: datetime):
    logger.info("Starting feed check...")
    # Read the control list
    with open(control_file, "r") as controlFile:
        json_data = json.load(controlFile)
        prev_products = {k: Entry(**json_data[k]) for k in json_data}

    # Fetch the feed again, and again, and again...
    f = feedparser.parse(feed_url, agent=user_agent)

    # Compare feed entries to control list.
    # If there are new entries, send a message/push
    # and add the new entry to new control list.
    # TODO remove this line once code is working
    await client.get_channel(channel_id).send("Checking feed...")

    current_products = {}
    # Convert the JSON array to a list of Product objects
    new_products = [Entry(**{name: p.get(name) for name in field_names}) for p in f.entries]
    # Create a dictionary of the new products
    for product in new_products:
        current_products[product.id] = product
    added_products = {k: v for k, v in current_products.items() if k not in prev_products}
    removed_products = {k: v for k, v in prev_products.items() if k not in current_products}
    message = prepareMessage(added_products, removed_products, current_products, next_update)
    if message:
        await client.get_channel(channel_id).send(message)
    prev_products = current_products

    # Write the new control list to the control file
    with open(control_file, "w") as controlFile:
        json.dump(prev_products, controlFile, indent=4, cls=EntryEncoder)
    logger.info(
        f"Checking done! warned for {len(added_products)} new items, and {len(removed_products)} removed items. Currently have {len(current_products)} items."
    )
    # print next update time, full info (hour:minute timezone on the day.month)
    logger.info(f"Next check at {next_update.strftime('%H:%M %Z on the %d.%m')}")


# Activate the discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logger.info(f"{client.user} has connected to Discord!")
    iter = croniter(cron_string, datetime.now(tz=timezone))
    next_update = iter.get_next(datetime)
    # Start the loop
    try:
        while True:
            now = datetime.now(tz=timezone)
            time_remaining = (next_update - now).total_seconds()
            if time_remaining <= 0:
                # If the scheduled time has passed, update immediately
                await feedWatcher(next_update)
                iter = croniter(cron_string, datetime.now(tz=timezone))
                next_update = iter.get_next(datetime)
            else:
                # If there is time remaining until the scheduled time, sleep for that duration
                logger.info(f"Main func Sleeping until {next_update.strftime('%H:%M %Z on the %d.%m')}")
                await asyncio.sleep(time_remaining)
    except Exception as e:
        logger.error(f"Error in feedWatcher: {e}")


# Main program
def main():
    # Setup the control list if it does not exist
    if not os.path.isfile(control_file):
        logger.info("Doing initial setup...")
        # Set control to blank list
        control = {}

        # Write the list to a json file for later use
        with open(control_file, "w") as outfile:
            json.dump(control, outfile)

    logger.info("Starting feed check App...")
    client.run(token)


if __name__ == "__main__":
    main()
