from pathlib import Path
from typing import overload

from spacy.tokens import Doc


class LanguageModel:

    def __init__(self, order: int, path):
        self.order = order
        self.path = path

    def to_disk(self, path=None):
        pass

    def from_disk(self, path=None):
        v: int or str = "a"
        if isinstance(v, str):
            print("a")
        pass

    @overload
    def calc_held_out(self, corpus: [Doc]):
        ...

    @overload
    def calc_held_out(self, corpus: Path):
        ...

    def calc_held_out(self, corpus):
        pass




