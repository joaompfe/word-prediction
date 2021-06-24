# CETEMPúblico data processing scripts

Scripts to process the CETEMPúblico `CETEMPublico1.7.txt` file, available for downloading from [https://www.linguateca.pt/ACDC/](https://www.linguateca.pt/ACDC/).

`raw2xml.sh` generates a valid XML version of the corpus.

`xml2json.sh` generates a JSON version of the corpus`(from the valid XML version) compatible with spaCy.

`xml2sl.pl` generates a simple ("sentence per line") version of the corpus from the valid XML version.

`sl2spacy.py` divides the corpus (from the "sentence per line" version) in several files in spaCy binary format (spaCy 
suffers if dealing with the corpus all at once).