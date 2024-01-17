# Movie Notifier Discord Bot

## Overview
A Discord bot that sends notifications on news, announcements, and release info related to movies and the film industry.

## Features
- **Upcoming Movie Notifications**: Receive timely notifications about new movie releases.

## Requirements
- Python 3.7 or higher
- Discord.py library (`pip install discord.py`)
- TMDB API Key (Sign up at [TMDB](https://www.themoviedb.org/) to get an API key)

## Setup
1. Clone the repository.
2. Install dependencies: ```pip install -r requirements.txt```
3. Configure the bot:
    - Create a Discord bot and obtain the token from the [Discord Developer Portal](https://discordapp.com/developers/applications/).
    - Insert your Discord bot token and TMDB API key in an .env file in the same directory as the code.
4. Run the bot on a server: ```python bot.py```

## Usage
- The bot will automatically send messages to the channel about new movie releases daily by default.

## Acknowledgements
This bot uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB.
