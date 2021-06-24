import os
import sys
from subprocess import run

from spacy.lang.pt import Portuguese
from spacy.tokens import DocBin
from tqdm import tqdm


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_dir = sys.argv[2]
    result = run("wc -l < %s" % in_path, shell=True, capture_output=True)
    n_lines = int(result.stdout)

    print(in_path)

    doc_bin = DocBin()
    nlp = Portuguese()

    max_length = 5e5
    i = 1
    part = 0  # `doc_bin` is saved in batches/parts of `max_length` sentences each, to avoid memory issues

    def out_path():
        return out_dir + "/" + os.path.splitext(os.path.basename(in_path))[0] + "-part" + str(part) + ".spacy"

    print(out_path)

    with open(in_path, encoding="ISO-8859-1") as f:
        for line in tqdm(f, desc="Converting 'sentence per line' format to spacy binary format", total=n_lines):
            doc = nlp(line.rstrip())
            doc_bin.add(doc)

            if not i % max_length:
                doc_bin.to_disk(out_path())
                part += 1
                doc_bin = DocBin()  # create an new empty doc to free memory
            i += 1
    doc_bin.to_disk(out_path())
