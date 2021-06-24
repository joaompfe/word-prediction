from spacy.lang.pt import Portuguese

from wp import BigramComponent, calc_grams
import pickle


@Portuguese.factory("next_word_predictor")
def create_next_word_predictor(nlp, name):
    if name == "bigram":
        return BigramComponent()


def test_next_word_predictor():
    nlp = Portuguese()
    nlp.add_pipe("next_word_predictor", "bigram")
    nlp.from_disk("models", exclude=["tokenizer"])

    my_doc = nlp("Uma vez")
    print(my_doc._.next_word_pred)


def calc_and_save_bigrams():
    ngrams = calc_grams(2, Portuguese(), "data/corpus/test/train-%s.spacy")
    f = open('./models/bigram/tmp.pkl', 'wb+')
    pickle.dump(ngrams, f)
    f.close()
