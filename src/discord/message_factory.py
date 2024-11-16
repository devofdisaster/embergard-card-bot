from ast import List

from pandas import DataFrame

from discord import Embed
from src.discord.custom_icons import Icons
from src.discord.replacement_icon_map import icon_map


def generate_single_embed(frame: DataFrame) -> Embed:
    embed = Embed(
        title=frame["Name"].array[0],
        description=_build_single_description(frame),
    )
    embed.set_thumbnail(url=_thumbnail_link(frame))
    embed.set_footer(text=_build_footer(frame))

    return embed


def generate_multi_embed(card_frame: DataFrame, warband_frame: DataFrame) -> Embed:
    embed = Embed()
    card_names = card_frame["Name"].tolist()
    warband_names = warband_frame["Name"].tolist()

    for i in range(0, min(len(card_names), 24), 5):
        embed.add_field(
            name="Cards",
            value="\n".join(card_names[i : i + 5]),
            inline=True,
        )

    fields_left = 25 - len(embed.fields)

    for i in range(0, min(len(warband_names), fields_left), 5):
        embed.add_field(
            name="Warbands",
            value="\n".join(warband_names[i : i + 5]),
            inline=True,
        )

    return embed


def generate_warscroll_embed(frame: DataFrame) -> Embed:
    embed = Embed(
        title=frame["Name"].array[0],
    ).set_image(url=_warband_image_link(frame))

    return embed


def generate_warband_embed(frame: DataFrame) -> Embed:
    warscroll = frame[frame["WarscrollType"].notnull()]
    fighter_names = frame[frame["WarscrollType"].isnull()]["Name"].tolist()

    embed = Embed(
        title=warscroll["Name"].array[0],
    ).set_image(url=_warband_image_link(warscroll))

    for i in range(0, len(fighter_names), 5):
        embed.add_field(
            name="Fighters",
            value="\n".join(fighter_names[i : i + 5]),
            inline=True,
        )

    return embed


def generate_alliance_warband_embeds(frame: DataFrame) -> Embed:
    warscrolls = frame[frame["WarscrollType"].notnull()]
    fighters = frame[frame["WarscrollType"].isnull()]
    fighter_names = fighters["Name"].tolist()
    fighter_list = Embed(
        title=fighters["Warband"].array[0],
    ).set_image(url=_warband_image_link(warscrolls.iloc[[0]]))

    for i in range(0, len(fighter_names), 5):
        fighter_list.add_field(
            name="Fighters",
            value="\n".join(fighter_names[i : i + 5]),
            inline=True,
        )

    embeds = [fighter_list]

    for j in range(1, len(warscrolls)):
        embeds.append(Embed().set_image(url=_warband_image_link(warscrolls.iloc[[j]])))

    return embeds


def generate_fighter_embeds(frame: DataFrame) -> List:
    warband_name = frame["Warband"].array[0]

    return [
        Embed(title=frame["Name"].array[0]).set_image(url=_warband_image_link(frame)),
        Embed()
        .set_image(url=_warband_image_link(frame, inspired=True))
        .set_footer(text=f"Warband: {warband_name}"),
    ]


def _build_single_description(frame: DataFrame) -> str:
    return f"{_build_icons(frame)}\n{_replace_description_icons(frame)}"


def _build_icons(frame: DataFrame) -> str:
    type_value = frame["Type"].array[0]

    if type_value == "Objective":
        return _build_objective_icons(frame)

    if type_value == "Ploy":
        return _build_ploy_icons(frame)

    if type_value == "Upgrade":
        return _build_upgrade_icons(frame)

    return ":question:"


def _build_objective_icons(frame: DataFrame) -> str:
    glory = int(frame["Glory/Cost"].array[0])
    add_surge = "Surge" == frame["ObjType"].array[0]
    obj_string = f"{Icons.OBJECTIVE.value}{Icons.SURGE.value if add_surge else ''}"
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
    set_name = frame["Set"].array[0].lower().replace(" ", "-")

    deck_name = (
        frame["Deck"].array[0].lower().replace(" rivals deck", "").replace(" ", "%20")
    )
    card_name = frame["Name"].array[0].replace(" ", "-").replace("'", "")
    file_name = f"{card_name}.png"

    return f"https://www.underworldsdb.com/cards/{set_name}/{deck_name}/{file_name}"


def _warband_image_link(frame: DataFrame, inspired: bool = False) -> str:
    warband_name = frame["Warband"].array[0].replace(" ", "-").replace("'", "").lower()
    image_number = frame["ImageNumber"].array[0]
    file_name = f"{warband_name}-{image_number}{'-inspired' if inspired else ''}.png"

    if "alliance" == frame["WarscrollType"].array[0]:
        warband_name = warband_name.replace("grand-alliance-", "")
        file_name = f"{warband_name}-0{image_number}.png"

    return f"https://www.underworldsdb.com/cards/fighters/{file_name}"


def _build_footer(frame: DataFrame) -> str:
    set_name = frame["Set"].array[0]
    deck_name = frame["Deck"].array[0]

    return f"Set: {set_name}, Deck: {deck_name}"
