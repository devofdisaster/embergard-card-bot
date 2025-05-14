from fuzzywuzzy import fuzz, process
from pandas import DataFrame, isna, read_csv


class Library:
    def __init__(self, card_path: str = None, warband_path: str = None):
        self._card_memory = None
        self._warband_memory = None
        self._card_path = card_path
        self._warband_path = warband_path

    def load(self) -> None:
        self._card_memory = read_csv(self._card_path)
        self._warband_memory = read_csv(self._warband_path)

    def search_cards(self, query: str) -> DataFrame:
        if not isinstance(self._card_memory, DataFrame):
            self.load()

        lowercase_query = query.lower().replace("’", "'")
        card_names = self._card_memory["Name"].drop_duplicates().tolist()
        extracted = process.extract(
            lowercase_query, card_names, scorer=fuzz.partial_ratio, limit=10
        )
        exactish_match_names = [
            match[0] for match in extracted if lowercase_query in match[0].lower()
        ]
        exact_match_names = [
            name for name in exactish_match_names if name.lower() == lowercase_query
        ]
        best_match_names = [match[0] for match in extracted if match[1] >= 80]

        return self._card_memory[
            self._card_memory["Name"].isin(
                exact_match_names
                if 1 == len(exact_match_names)
                else (
                    exactish_match_names
                    if 1 == len(exactish_match_names)
                    else best_match_names
                )
            )
        ].drop_duplicates(subset="Name")

    def find_deck_sets(self, frame: DataFrame) -> DataFrame:
        duplicates = self._card_memory[
            self._card_memory["Name"] == frame["Name"].array[0]
        ]

        return duplicates[["Set", "Deck"]]

    def search_warbands(self, query: str) -> DataFrame:
        if not isinstance(self._warband_memory, DataFrame):
            self.load()

        lowercase_query = query.lower().replace("’", "'")
        warband_names = self._warband_memory["Name"].tolist()
        extracted = process.extract(
            lowercase_query, warband_names, scorer=fuzz.partial_ratio, limit=10
        )
        exactish_match_names = [
            match[0] for match in extracted if lowercase_query in match[0].lower()
        ]
        exact_match_names = [
            name for name in exactish_match_names if name.lower() == lowercase_query
        ]
        best_match_names = [match[0] for match in extracted if match[1] >= 80]

        return self._warband_memory[
            self._warband_memory["Name"].isin(
                exact_match_names
                if 1 == len(exact_match_names)
                else (
                    exactish_match_names
                    if 1 == len(exactish_match_names)
                    else best_match_names
                )
            )
        ]

    def get_whole_warband(
        self, warband_name: str, grand_alliance: str = None
    ) -> DataFrame:
        if not isinstance(self._warband_memory, DataFrame):
            self.load()

        lowercase_warband_name = warband_name.lower()

        if grand_alliance is None:
            return self._warband_memory[
                [
                    lowercase_warband_name in value.lower()
                    for value in self._warband_memory["Warband"]
                ]
            ]

        lowercase_alliance_name = grand_alliance.lower()

        return self._warband_memory[
            [
                (
                    lowercase_warband_name in row["Warband"].lower()
                    and isna(row["WarscrollType"])
                )
                or (
                    lowercase_alliance_name in row["Warband"].lower()
                    and row["WarscrollType"] == "alliance"
                )
                for _, row in self._warband_memory[
                    ["Warband", "WarscrollType"]
                ].iterrows()
            ]
        ]
