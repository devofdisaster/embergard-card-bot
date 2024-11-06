import logging
import logging.handlers
import os

from discord import Client, Embed, Intents, Message

from src.card_library import Library


class EmbergardClient(Client):
    def __init__(self):
        self._log_handler = logging.handlers.RotatingFileHandler(
            filename=os.path.join(os.getcwd(), "logs", "embergard-bot.log"),
            encoding="utf-8",
            maxBytes=16 * 1024 * 1024,
            backupCount=5,
        )
        self._library = Library(
            path=os.path.join(os.getcwd(), "src", "resources", "library.csv")
        )

        intents = Intents().default()
        intents.message_content = True

        super().__init__(intents=intents)

    def run(self):
        return super().run(
            os.getenv("CLIENT_TOKEN"),
            log_handler=self._log_handler,
            log_level=logging.DEBUG,
        )

    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if message.content.startswith("((") and message.content.endswith("))"):
            content = message.content.lstrip("( \t").rstrip(" )\t")

            if 0 == len(content):
                return

            names = self._library.search(content)

            if 0 == len(names):
                return await message.channel.send("No matches found, mate")

            if 1 == len(names):
                embed = Embed(title=names[0])
                embed.add_field(
                    name="",
                    value="Some Card Text",
                    inline=False,
                )

                return await message.channel.send(embed=embed)

            embed = Embed()
            embed.add_field(
                name="Cards",
                value="\n".join(names),
                inline=True,
            )

            await message.channel.send(embed=embed)
