## Docs

### Requirements
- Linux platform
- [Poetry](https://python-poetry.org/)

### Installation 
Download the project from the repository:\
`git clone https://github.com/joaompfe/word-prediction`\
`cd word-prediction`

Install the project:\
`poetry install`

If you want to download the corpus data (approx. 4GB):\
`poetry run download-data`

If you want to download some pre-built portuguese language models (approx. 1GB):\
`poetry run download-models`

### Usage
Start a python shell using the poetry virtual env:\
`poetry run python`

Create a text-processing pipeline, e.g.:
```python
from spacy.lang.pt import Portuguese
nlp = Portuguese()
```

Create a predictor pipeline component and add it to the pipe:
```python
from word_prediction.nwp import TrigramLmWordPredictor
from word_prediction.trie import Trie

@Portuguese.factory("next_word_predictor")
def create_next_word_predictor(nlp, name):
    order = 3
    t = Trie(order, "models/train-mkn-trie")  # this model will only be available if you download the pre-built models
    nwp_pipe_component = TrigramLmWordPredictor(t)
    return nwp_pipe_component

nlp.add_pipe("next_word_predictor")
```

Process some sentences and see the next word predictions:
```python
sentences = ["seria útil", "amanhã e", "além de", "com muita"]
for s in sentences:
    doc = nlp(s)
    print("'%s' next word prediction is: '%s'" % (s, doc._.nwp))
```
