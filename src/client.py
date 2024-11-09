import logging
import logging.handlers
import os

from discord import Client, Intents, Message
from src.card_library import Library
from src.discord.message_factory import (
    generate_multi_embed,
    generate_single_embed,
    generate_warband_embed,
)


class EmbergardClient(Client):
    def __init__(self):
        self._log_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(os.getcwd(), "logs", "embergard-card-bot.log"),
            encoding="utf-8",
            maxBytes=16 * 1024 * 1024,
            backupCount=5,
        )
        self._library = Library(
            card_path=os.path.join(os.getcwd(), "src", "resources", "library.csv"),
            warband_path=os.path.join(os.getcwd(), "src", "resources", "warbands.csv"),
        )

        intents = Intents().default()
        intents.message_content = True

        super().__init__(intents=intents)

    def run(self) -> None:
        token = os.getenv("CLIENT_TOKEN")

        if not token:
            print(
                "No token found in environment variables, CLIENT_TOKEN needs to be set"
            )

            return

        return super().run(
            token,
            log_handler=self._log_handler,
            log_level=logging.DEBUG,
        )

    async def on_ready(self) -> None:
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: Message) -> None:
        if message.author == self.user:
            return

        if message.content.startswith("((") and message.content.endswith("))"):
            content = message.content.lstrip("( \t").rstrip(" )\t")

            if len(content) < 3:
                return await message.channel.send(
                    "Search term too short, must be at least Tok-long"
                )

            if 0 == len(content):
                return

            warband_matches = self._library.search_warbands(content)
            card_matches = self._library.search_cards(content)
            warband_count = len(warband_matches)
            card_count = len(card_matches)

            if 1 == warband_count and 0 == card_count:
                if 1 == int(warband_matches["IsWarscroll"].array[0]):
                    return await message.channel.send(
                        embed=generate_warband_embed(
                            self._library.get_whole_warband(
                                warband_matches["Warband"].array[0]
                            )
                        )
                    )

                return await message.channel.send(
                    embed=generate_warband_embed(warband_matches),
                )

            if 0 == warband_count and 1 == card_count:
                return await message.channel.send(
                    embed=generate_single_embed(card_matches)
                )

            if 0 == warband_count and 0 == card_count:
                return await message.channel.send("No matches found")

            await message.channel.send(
                embed=generate_multi_embed(card_matches, warband_matches)
            )
