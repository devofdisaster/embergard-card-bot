from pandas import DataFrame

from discord import Embed
from src.discord.custom_icons import Icons
from src.discord.uwdb_to_bot_icon_map import icon_map


def generate_single_embed(frame: DataFrame) -> Embed:
    embed = Embed(
        title=frame["Name"].array[0],
        description=_build_single_description(frame),
    )
    embed.set_thumbnail(url=_thumbnail_link(frame))
    embed.set_footer(text=_build_footer(frame))

    return embed


def generate_multi_embed(frame: DataFrame) -> Embed:
    embed = Embed()
    names = frame["Name"].tolist()

    for i in range(0, min(len(names), 24), 5):
        embed.add_field(
            name="Cards",
            value="\n".join(names[i : i + 5]),
            inline=True,
        )

    return embed


def _build_single_description(frame: DataFrame) -> str:
    return f"{_build_icons(frame)}\n{_replace_description_icons(frame)}"


def _build_icons(frame: DataFrame) -> str:
    match frame["Type"].array[0]:
        case "Objective":
            return _build_objective_icons(frame)
        case "Ploy":
            return _build_ploy_icons(frame)
        case "Upgrade":
            return _build_upgrade_icons(frame)
        case _:
            return ":question:"


def _build_objective_icons(frame: DataFrame) -> str:
    glory = int(frame["Glory/Cost"].array[0])
    add_surge = "Surge" == frame["ObjType"].array[0]
    obj_string = f"{Icons.OBJECTIVE.value}{':zap:' if add_surge else ''}"
    glories_string = (" - " + Icons.GLORY.value * glory) if glory else ""

    return obj_string + glories_string + "\n"


def _build_ploy_icons(frame: DataFrame) -> str:
    return f"{Icons.PLOY.value}\n"


def _build_upgrade_icons(frame: DataFrame) -> str:
    glory = int(frame["Glory/Cost"].array[0])
    glories_string = (" - " + Icons.GLORY.value * glory) if glory else ""

    return Icons.UPGRADE.value + glories_string + "\n"


def _replace_description_icons(frame: DataFrame) -> str:
    description = frame["Description"].array[0]

    for uwdb_icon, custom_icon in icon_map.items():
        description = description.replace(uwdb_icon, custom_icon).replace("\\n", "\n")

    return description


def _thumbnail_link(frame: DataFrame) -> str:
    card = frame.head(1)
    set_name = card["Set"].array[0].lower().replace(" ", "-")

    deck_name = (
        card["Deck"].array[0].lower().replace(" rivals deck", "").replace(" ", "%20")
    )
    card_name = card["Name"].array[0].replace(" ", "-")
    file_name = f"{card_name}.png"

    return f"https://www.underworldsdb.com/cards/{set_name}/{deck_name}/{file_name}"


def _build_footer(frame: DataFrame) -> str:
    set_name = frame["Set"].array[0]
    deck_name = frame["Deck"].array[0]

    return f"Set: {set_name}, Deck: {deck_name}"
