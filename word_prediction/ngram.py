import ngram_lm.trie
import ngram_lm.word
from spacy.tokens import Doc, SpanGroup

from word_prediction.lm import LanguageModel


def ngrams(n: int, doc: Doc) -> SpanGroup:
    span_group = SpanGroup(doc, name="%d-grams" % n)
    for i in range(doc.__len__() - n + 1):
        span_group.append(doc[i:i+n])
    return span_group


class NgramComponent:
    def __init__(self, n: int):
        self.n = n

    def __call__(self, doc: Doc) -> Doc:
        name = "%d-grams" % self.n
        doc.spans[name] = ngrams(self.n, doc)
        return doc


class NgramWordPredictor(NgramComponent):
    """Pipeline component for next word prediction by n-gram model"""

    def __init__(self, lm: LanguageModel, n: int):
        super(NgramWordPredictor, self).__init__(n)
        # self.ngrams_count = {}
        self.lm = lm
        # self.lm = ngram_lm.trie.Trie(str(lm_path))
        if not Doc.has_extension("nwp"):
            Doc.set_extension("nwp", default=[])

    def __call__(self, doc: Doc) -> Doc:
        doc = super(NgramWordPredictor, self).__call__(doc)
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


class BigramWordPredictor(NgramWordPredictor):
    def __init__(self, lm: LanguageModel):
        super(BigramWordPredictor, self).__init__(lm, 2)


class TrigramWordPredictor(NgramWordPredictor):
    def __init__(self, lm: LanguageModel):
        super(TrigramWordPredictor, self).__init__(lm, 3)
