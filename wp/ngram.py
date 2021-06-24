import pickle

from spacy import Language
from spacy.tokens import Doc, DocBin
import nltk
import os.path

from tqdm import tqdm


class NgramComponent:
    """Pipeline component for next word prediction by n-gram model"""

    def __init__(self, n: int):
        self.n = n
        self.ngrams = {}
        if not Doc.has_extension("words_prob"):
            Doc.set_extension("words_prob", default=[])
        if not Doc.has_extension("next_word_pred"):
            Doc.set_extension("next_word_pred", default=[])

    def __call__(self, doc: Doc) -> Doc:
        n = self.n
        doc._.words_prob = {}
        doc._.next_word_pred = None

        s_contexts = nltk.ngrams(doc.text.split(), n - 1)
        s_contexts = [c for c in s_contexts]
        context = s_contexts[-1]
        try:
            next_words = self.ngrams[context]
            count_sum = sum(next_words.values())
            doc._.words_prob = {word: count / count_sum for word, count in next_words.items()}
            doc._.next_word_pred = max(doc._.words_prob, key=doc._.words_prob.get)
        except KeyError:
            pass

        return doc

    def to_disk(self, path, exclude=tuple()):
        f = open(path / "data.pkl", "wb")
        pickle.dump(self.ngrams, f)
        f.close()

    def from_disk(self, path, exclude=tuple()):
        f = open(path / "data.pkl", 'rb')
        ngrams = pickle.load(f)
        self.ngrams = ngrams
        f.close()
        return self


class BigramComponent(NgramComponent):
    def __init__(self):
        super(BigramComponent, self).__init__(2)


def calc_grams(n: int, lang: Language, corpus_path):
    part = 0
    ngrams = {}
    while os.path.isfile(corpus_path % "part%d" % part):
        corpus = DocBin()
        corpus.from_disk(corpus_path % "part%d" % part)
        corpus = corpus.get_docs(lang.vocab)

        for sentence in tqdm(corpus, desc="Calculating grams for part %d of the corpus" % part):
            s_ngrams = nltk.ngrams(sentence.text.split(), n)

            for gram in s_ngrams:
                context = gram[0:n - 1]
                last_word = gram[-1]
                if context in ngrams:
                    if last_word in ngrams[context]:
                        ngrams[context][last_word] += 1
                    else:
                        ngrams[context][last_word] = 1
                else:
                    ngrams[context] = {last_word: 1}
        part += 1
    return ngrams
