# DiscordPiBot

A discord bot i use to warn me about different things. It currently warns me about :

-   new raspberry pis availability using the rpilocator.com rss feed

# Installation

-   First install all requirements with poetry (`poetry install`)
-   Then set the settings.yaml file with all your personnal info. You can use [the example file](settings_example.yaml) as a reference. You need to set mainly :
    -   Your token id for your bot
    -   The channel id where you want the bot to send messages
-   Run it with poetry (`poetry run discordpibot`)

You can also use docker to run the bot. To do so, you need to run the following command :

```bash
docker-compose up -d
```
