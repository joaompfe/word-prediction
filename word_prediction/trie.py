import pickle
from pathlib import Path

import ngram_lm.trie
import ngram_lm.word
from spacy.lang.pt import Portuguese
from spacy.tokens import Doc
from tqdm import tqdm

from word_prediction.ngram import NgramLm
from word_prediction.nwp import NextWordPredictor


class Trie(NgramLm, NextWordPredictor):
    _c_trie: ngram_lm.trie.Trie

    def __init__(self, order: int, path):
        super().__init__(order, path)
        self._c_trie = ngram_lm.trie.Trie(str(path))

    def nwp(self, context):
        word: ngram_lm.word.Word = self._c_trie.next_word_predictions([str(gram) for gram in context])[0]
        return word

    def to_disk(self, path=None):
        if path is None:
            path = self.path
        self._c_trie.to_disk(str(path))

    def from_disk(self, path=None):
        if path is None:
            path = self.path
        self._c_trie.from_disk(str(path))

    def k_test(self, test_set, k):
        if isinstance(test_set, Path) or isinstance(test_set, str):
            with open(test_set, "r") as f:
                docs = list()
                nlp = Portuguese()  # TODO create lang attribute in LanguageModel
                for line in f:
                    docs.append(nlp(line))
        elif isinstance(test_set, list) and isinstance(test_set[0], Doc):
            docs = test_set
        else:
            raise ValueError

        result = k * [0]
        total = 0
        for doc in tqdm(docs):
            sentence = str(doc).split()
            sen_len = len(sentence)
            for i in range(sen_len - self.order - 2):
                words = sentence[i:i + self.order - 1]
                next_word = sentence[i + self.order - 1]
                nwp = self._c_trie.next_word_predictions([str(w) for w in words], k)
                pos = None
                for j, pred in enumerate(nwp):
                    if str(pred) == str(next_word):
                        pos = j
                if pos is not None:
                    result[pos] += 1
                total += 1
        return result, total


def build(order: int, arpa_path: str, out_path: str):
    ngram_lm.trie.build(order, arpa_path, out_path)


def k_test(trie_path, order, test_set, k):
    t = Trie(order, trie_path)
    result, total = t.k_test(test_set, k)
    with open("result-ml.pickle", "wb") as f:
        pickle.dump(result, f)
    for r in result:
        print(r/total)
    print(total)
