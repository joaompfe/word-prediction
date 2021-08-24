import ngram_lm.trie
import ngram_lm.word
import spacy.tokens

from word_prediction.lm import LanguageModel


class Trie(LanguageModel):
    _c_trie: ngram_lm.trie.Trie

    def __init__(self, path):
        super().__init__(path)
        self._c_trie = ngram_lm.trie.Trie(str(path))

    def nwp(self, context: [str] or spacy.tokens.SpanGroup):
        word: ngram_lm.word.Word = self._c_trie.next_word_prediction([str(gram) for gram in context])
        return word

    def to_disk(self, path=None):
        if path is None:
            path = self.path
        self._c_trie.to_disk(str(path))

    def from_disk(self, path=None):
        if path is None:
            path = self.path
        self._c_trie.from_disk(str(path))


def build(order: int, arpa_path: str, out_path: str):
    ngram_lm.trie.build(order, arpa_path, out_path)
