from pathlib import Path
from typing import overload, Union

import ngram_lm.trie
import ngram_lm.word
from spacy.tokens import Doc, SpanGroup

from word_prediction.lm import LanguageModel
from word_prediction.ngram import ngrams


class NextWordPredictor:

    @overload
    def nwp(self, context: [str]) -> ngram_lm.word.Word:
        ...

    @overload
    def nwp(self, context: SpanGroup) -> ngram_lm.word.Word:
        ...

    def nwp(self, context: SpanGroup) -> ngram_lm.word.Word:
        pass

    @overload
    def k_test(self, test_set: Path, k):
        ...

    def k_test(self, test_set: [Doc], k):
        pass


class NgramComponent:
    def __init__(self, n: int):
        self.n = n

    def __call__(self, doc: Doc) -> Doc:
        name = "%d-grams" % self.n
        doc.spans[name] = ngrams(self.n, doc)
        return doc


class NgramLmWordPredictor(NgramComponent):
    """Pipeline component for next word prediction by n-gram model"""

    def __init__(self, lm: Union[LanguageModel, NextWordPredictor], n: int):
        super(NgramLmWordPredictor, self).__init__(n)
        self.lm = lm
        if not Doc.has_extension("nwp"):
            Doc.set_extension("nwp", default=[])

    def __call__(self, doc: Doc) -> Doc:
        doc = super(NgramLmWordPredictor, self).__call__(doc)
        n = self.n
        doc._.nwp = None

        doc_ngrams = ngrams(n - 1, doc)
        doc_last_ngram = doc_ngrams[-1]
        word: ngram_lm.word.Word = self.lm.nwp(doc_last_ngram)
        doc._.nwp = word

        return doc

    def to_disk(self, path, exclude=tuple()):
        self.lm.to_disk()

    def from_disk(self, path, exclude=tuple()):
        self.lm.from_disk()
        return self


class BigramLmWordPredictor(NgramLmWordPredictor):
    def __init__(self, lm: LanguageModel):
        super(BigramLmWordPredictor, self).__init__(lm, 2)


class TrigramLmWordPredictor(NgramLmWordPredictor):
    def __init__(self, lm: LanguageModel):
        super(TrigramLmWordPredictor, self).__init__(lm, 3)
