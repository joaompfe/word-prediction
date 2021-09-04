from spacy.tokens import Doc, SpanGroup

from word_prediction.lm import LanguageModel


class NgramLm(LanguageModel):
    pass


def ngrams(n: int, doc: Doc) -> SpanGroup:
    span_group = SpanGroup(doc, name="%d-grams" % n)
    for i in range(doc.__len__() - n + 1):
        span_group.append(doc[i:i+n])
    return span_group
