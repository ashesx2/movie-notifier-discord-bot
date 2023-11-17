"""
Module for Movie Notifier Discord Bot.

The Discord bot sends notifications on upcoming movie releases.
"""
from datetime import date, timedelta
import logging
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import tmdb_api_util


# Load tokens.
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup loggers.
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8")
file_formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
file_handler.setFormatter(file_formatter)

logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


class MovieBot(commands.Bot):
    """
    This Discord bot fetches movie data from TMDB and
    sends messages to a Discord channel to notify users
    about upcoming movie releases.
    """
    def __init__(self) -> None:
        """
        Initializes Discord bot. 
        """
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.default()
        )
        self.logger = logger

    async def on_ready(self) -> None:
        """
        Prints a message to indicate its online status.
        Additionally starts checking for upcoming movies.
        """
        self.logger.info("%s has connected to Discord!", self.user.name)
        self.check_upcoming_releases.start()

    async def send_movie_notification(self, movie_id: int) -> None:
        """
        Send a notification of an upcoming movie release to Discord.

        Args:
            movie_id: Integer value of movie in TMDB.
        """
        movie = tmdb_api_util.get_movie_details(movie_id)

        # TODO: Figure out where and how the notifications should be sent.
        channel = self.get_channel(1171157889986076787)

        # TODO: Send more info about the info besides basic information.
        message = f"Upcoming: {movie["title"]} on {movie["release_date"]}"
        self.logger.info(
            "Sending message to channel %s: '%s'",
            channel.name,
            message
        )
        await channel.send(message)

    @tasks.loop(hours=24)
    async def check_upcoming_releases(self) -> None:
        """
        Check for upcoming movie releases daily and send notifications.
        """
        # TODO: Store this information in a file to better track/update
        # upcoming movies and send only new notifications.
        self.logger.info("Checking upcoming movies.")
        upcoming_movies = tmdb_api_util.fetch_upcoming_movies()

        # Filter movies that will be released within the next week.
        today = date.today()
        new_releases = []
        for movie_id, release_date in upcoming_movies:
            if today <= release_date <= today + timedelta(days=7):
                self.logger.info("Found new release (movie ID %d).", movie_id)
                new_releases.append(movie_id)

        # Send a notification for each upcoming release.
        for movie_id in new_releases:
            await self.send_movie_notification(movie_id)

        self.logger.info("Finished checking upcoming movies.")


bot = MovieBot()
bot.run(TOKEN)
