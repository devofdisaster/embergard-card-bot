import pandas as pd


class Library:
    def __init__(self, path: str = None):
        self._memory = None
        self._path = path

    def load(self):
        self._memory = pd.read_csv(self._path)

    def search(self, query: str):
        if not isinstance(self._memory, pd.DataFrame):
            self.load()

        lowercase_query = query.lower()
        matches = self._memory[
            [lowercase_query in value.lower() for value in self._memory["Name"]]
        ]

        return matches["Name"].tolist()
