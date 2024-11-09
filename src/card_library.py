from pandas import DataFrame, read_csv


class Library:
    def __init__(self, path: str = None):
        self._memory = None
        self._path = path

    def load(self) -> None:
        self._memory = read_csv(self._path)

    def search(self, query: str) -> DataFrame:
        if not isinstance(self._memory, DataFrame):
            self.load()

        lowercase_query = query.lower()
        matches = self._memory[
            [lowercase_query in value.lower() for value in self._memory["Name"]]
        ].drop_duplicates(subset=["Name"])

        exact_matches = matches[
            [lowercase_query == value.lower() for value in matches["Name"]]
        ]

        if 1 == len(exact_matches):
            return exact_matches

        return matches
