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
        matches = self._card_memory[
            [lowercase_query in value.lower() for value in self._card_memory["Name"]]
        ].drop_duplicates(subset=["Name"])

        exact_matches = matches[
            [lowercase_query == value.lower() for value in matches["Name"]]
        ]

        if 1 == len(exact_matches):
            return exact_matches

        return matches

    def search_warbands(self, query: str) -> DataFrame:
        if not isinstance(self._warband_memory, DataFrame):
            self.load()

        lowercase_query = query.lower().replace("’", "'")
        matches = self._warband_memory[
            [lowercase_query in value.lower() for value in self._warband_memory["Name"]]
        ]

        exact_matches = matches[
            [lowercase_query == value.lower() for value in matches["Name"]]
        ]

        if 1 == len(exact_matches):
            return exact_matches

        return matches

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
