# DiscordPiBot

A discord bot i use to warn me about different things. It currently warns me about :

-   new raspberry pis availability using the rpilocator.com rss feed

# Installation

-   First install all requirements with poetry (`poetry install`)
-   Then set the settings.yaml file with all your personnal info. You can use [the example file](settings_example.yaml) as a reference. You need to set mainly :
    -   Your token id for your bot
    -   The channel id where you want the bot to send messages
-   Launch the program using docker, docker compose (`docker-compose up -d --build`) or directly with python (`python3 main.py`)

# Improvements being made/to do :

-   Warn when an item is no longer available. Not really a priority but it would be nice to have
