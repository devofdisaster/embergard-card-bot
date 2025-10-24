import logging
import logging.handlers
import os
import re

from discord import Client, Intents, Message
from src.card_library import Library
from src.discord.email_helper import generate_mailto_link, parse_email_request
from src.discord.message_factory import (
    generate_alliance_warband_embeds,
    generate_email_embed,
    generate_fighter_embeds,
    generate_multi_embed,
    generate_single_embed,
    generate_warband_embed,
    generate_warscroll_embed,
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

        email_content_parsed = parse_email_request(message.content)

        if email_content_parsed is not None:
            subject, body = email_content_parsed

            embed = generate_email_embed(
                subject, body, generate_mailto_link(subject, body)
            )

            await message.channel.send(embed=embed)

            return

        matches = re.findall(r"\(\(\s?(.*?)\s?\)\)", message.content)
        match_count = len(matches)

        if 0 == match_count:
            return

        if 1 == match_count and "help" == matches[0].strip():
            return await self.send_help_message(message=message)

        for match in matches:
            query = match.strip()

            if 0 == len(query):
                return

            if len(query) < 3:
                if 1 == match_count:
                    return await message.channel.send(
                        "Search term too short, must be at least Tok-long"
                    )

                continue

            lowercase_query = query.lower().replace("’", "'")
            warband_matches = self._library.search_warbands(lowercase_query)
            card_matches = self._library.search_cards(lowercase_query)
            exactish_card_matches = card_matches[
                [lowercase_query in value.lower() for value in card_matches["Name"]]
            ]
            exactish_warband_matches = warband_matches[
                [lowercase_query in value.lower() for value in warband_matches["Name"]]
            ]
            warband_count = len(warband_matches)
            card_count = len(card_matches)

            if 0 == warband_count and 0 == card_count:
                await message.channel.send("No matches found")

                continue

            if (0 == warband_count and 1 == card_count) or (
                1 == len(exactish_card_matches)
            ):
                await message.channel.send(
                    embed=generate_single_embed(
                        card_matches, self._library.find_deck_sets(card_matches)
                    )
                )

                continue

            if (1 == warband_count and 0 == card_count) or (
                1 == len(exactish_warband_matches)
            ):
                if warband_matches["WarscrollType"].isnull().array[0]:
                    await message.channel.send(
                        embeds=generate_fighter_embeds(warband_matches),
                    )

                    continue

                if "alliance" == warband_matches["WarscrollType"].array[0]:
                    await message.channel.send(
                        embed=generate_warscroll_embed(warband_matches)
                    )

                    continue

                if "generic" == warband_matches["WarscrollType"].array[0]:
                    await message.channel.send(
                        embeds=generate_alliance_warband_embeds(
                            self._library.get_whole_warband(
                                warband_matches["Warband"].array[0],
                                warband_matches["GrandAlliance"].array[0],
                            )
                        )
                    )

                    continue

                await message.channel.send(
                    embed=generate_warband_embed(
                        self._library.get_whole_warband(
                            warband_matches["Warband"].array[0]
                        )
                    )
                )

                continue

            await message.channel.send(
                embed=generate_multi_embed(card_matches, warband_matches)
            )

    async def send_help_message(self, message: Message) -> None:
        help_text = (
            "**Card and Warband Search:**\n"
            "- Use **((search_term))** to search for cards or warbands, for example `((ghartok))`\n"
            "- Use multiple search terms in one message: `((ghartok)) ((fortitude)) ((pandaemonium)) ((alliance death))`\n\n"
            "**Rules Quertions Email Templating:**\n"
            "- Use **[[Subject]]** followed by message content to generate an email link:\n"
            "```\n[[Spitewood Q: New Tokens]]\nAre Aqua Ghyranis Feature Tokens, feature tokens?\nDo they count for the Countdown to Cataclysm tracker? Can Ghartok be driven back from one?```\n\n"
            "**Other:**\n"
            "- Use **((help))** to get this exceedingly helpful message"
        )
        await message.channel.send(help_text)
