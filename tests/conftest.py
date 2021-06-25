import pytest
from spacy.lang.pt import Portuguese


@pytest.fixture
def nlp():
    return Portuguese()


@pytest.fixture
def sentences():
    return ["seria útil", "amanhã", "nunca", "além de", "com muita", "desejo", "sempre", "com"]


@pytest.fixture
def docs(sentences, nlp):
    return list(nlp.pipe(sentences))
