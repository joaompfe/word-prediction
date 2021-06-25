import pytest
from spacy.lang.pt import Portuguese

from word_prediction.ngram import NgramComponent, BigramWordPredictor, TrigramWordPredictor


# @pytest.fixture
# def bigram_comp():
#     return NgramComponent(2)


@Portuguese.factory("bigram")
def create_bigram(nlp, name):
    return NgramComponent(2)


@pytest.fixture
def bigram_pipe(nlp):
    nlp.add_pipe("bigram")
    return nlp


def test_bigram(bigram_pipe, sentences):
    doc = bigram_pipe(sentences[0])
    assert "2-grams" in doc.spans
    assert doc.spans["2-grams"].__len__() == (doc.__len__() - 2 + 1)
    assert doc.spans["2-grams"][0].__len__() == 2


@Portuguese.factory("next_word_predictor")
def create_next_word_predictor(nlp, name):
    if name == "bigram":
        return BigramWordPredictor()
    elif name == "trigram":
        return TrigramWordPredictor()


def test_next_word_predictor(nlp, sentences):
    nlp.add_pipe("next_word_predictor", "bigram")
    nlp.from_disk("models", exclude=["tokenizer"])

    for s in sentences:
        my_doc = nlp(s)
        print("%s ... %s" % (s, my_doc._.next_word_pred))
