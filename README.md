# Dr. Isaac Kleiner Bot
This is the Discord bot for Summit Cinema's Discord server, based on the famous character Dr. Isaac Kleiner from the Half-Life series.

## Setting up

### Install dependencies
Simply run `pip install -r requirements.txt` in the top-most directory.

### Add bot token
The bot requires a `bot_constants.py` file in the top-most directory in order for the bot to run. This file contains the bot's Discord token.

It should be formatted like so:
```py
DISCORD_API_TOKEN = "TOKEN_GOES_HERE"
```

### Run the bot
Simply run `python3 bot_start.py`.

## Cogs
This Discord bot uses cogs to organize its commands into separate files.

Information about each bot's cog is given below.

### Info
Contains generalized commands that anyone can use.

### Moderation
Contains commands that only moderators and admins can use.

### Fun
Contains miscellaneous 'fun' commands which output various fun results.

### Images
An extension of 'fun' commands, contains commands that output an image result.

### Color Roles
Used to assign colored roles to users who are Nitro-boosting the Discord server.
