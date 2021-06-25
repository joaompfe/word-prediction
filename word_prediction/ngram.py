import pickle

from spacy import Language
from spacy.lang.pt import Portuguese
from spacy.tokens import Doc, DocBin, SpanGroup
import os.path

from tqdm import tqdm


def ngrams(n: int, doc: Doc) -> SpanGroup:
    span_group = SpanGroup(doc, name="%d-grams" % n)
    for i in range(doc.__len__() - n + 1):
        span_group.append(doc[i:i + n])

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

    def __init__(self, n: int):
        super(NgramWordPredictor, self).__init__(n)
        self.ngrams_count = {}
        if not Doc.has_extension("words_prob"):
            Doc.set_extension("words_prob", default=[])
        if not Doc.has_extension("next_word_pred"):
            Doc.set_extension("next_word_pred", default=[])

    def __call__(self, doc: Doc) -> Doc:
        doc = super(NgramWordPredictor, self).__call__(doc)
        n = self.n
        doc._.words_prob = {}
        doc._.next_word_pred = None

        doc_ngrams = ngrams(n - 1, doc)
        doc_last_ngram = doc_ngrams[-1]
        dict_node = self.ngrams_count
        try:
            # traverse the dictionary tree
            for gram in doc_last_ngram:
                dict_node = dict_node[gram.text]
            possible_next_words = dict_node
            count_sum = sum(possible_next_words.values())
            doc._.words_prob = {word: count / count_sum for word, count in possible_next_words.items()}
            doc._.next_word_pred = max(doc._.words_prob, key=doc._.words_prob.get)
        except KeyError:
            pass

        return doc

    def to_disk(self, path, exclude=tuple()):
        f = open(path / "data.pkl", "wb")
        pickle.dump(self.ngrams_count, f)
        f.close()

    def from_disk(self, path, exclude=tuple()):
        print("path: " + str(path))
        f = open(path / "data.pkl", 'rb')
        ngrams_count = pickle.load(f)

        dict_node = ngrams_count
        try:
            for i in range(self.n):
                dict_node = dict_node[list(dict_node.keys())[0]]
        except KeyError:
            raise ValueError("the loaded n-gram count dictionary has less depth than %d "
                             "(incompatible with %d-gram model)" % (self.n, self.n))
        if type(dict_node) is not int:
            raise ValueError("the loaded n-gram count dictionary has more depth than %d "
                             "(incompatible with %d-gram model)" % (self.n, self.n))

        self.ngrams_count = ngrams_count
        f.close()
        return self


class BigramWordPredictor(NgramWordPredictor):
    def __init__(self):
        super(BigramWordPredictor, self).__init__(2)


class TrigramWordPredictor(NgramWordPredictor):
    def __init__(self):
        super(TrigramWordPredictor, self).__init__(3)


def count_ngrams(n: int, lang: Language, corpus_path):
    part = 0
    ngrams_count = {}
    while os.path.isfile(corpus_path % "part%d" % part):
        corpus = DocBin()
        corpus.from_disk(corpus_path % "part%d" % part)
        corpus = corpus.get_docs(lang.vocab)

        for sentence in tqdm(corpus, desc="Calculating grams for part %d of the corpus" % part):
            sentence_ngrams = ngrams(n, sentence)

            for ngram in sentence_ngrams:
                dictionary = ngrams_count
                for gram in ngram:
                    if gram == ngram[-1]:
                        if gram.text in dictionary:
                            dictionary[gram.text] += 1
                        else:
                            dictionary[gram.text] = 1
                    else:
                        if gram.text not in dictionary:
                            dictionary[gram.text] = {}
                    dictionary = dictionary[gram.text]

        part += 1
    return ngrams_count


def count_and_save_ngrams(n: int, out_path: str, in_path="data/corpus/cetemp/train-%s.spacy", lang=Portuguese()):
    f = open(out_path, 'wb+')
    pickle.dump(count_ngrams(n, lang, in_path), f)
    f.close()
