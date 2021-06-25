#!/bin/bash

SCRIPTS_DIR="scripts/cetemp"
readonly SCRIPTS_DIR

echo "Warning: depending on the input file, this might take a while. For the CETEMPublico1.7, 1-2 hours should be required."

xml_file="$2/$(basename "$1").xml"
touch "$xml_file"

bash "$SCRIPTS_DIR/raw2xml.sh" "$1" "$xml_file"

sl_file="$2/$(basename "$1").sl"
touch "$sl_file"

perl "$SCRIPTS_DIR/xml2sl.pl" "$xml_file" "$sl_file"

poetry run python "$SCRIPTS_DIR/split_train_test_dev.py" "$sl_file" "$2"

#venv=$(poetry env info -p)
#( echo "#!$venv"; cat $SCRIPTS_DIR/sl2spacy.py; ) > $SCRIPTS_DIR/sl2spacy.py
#chmod +x $SCRIPTS_DIR/sl2spacy.py
#poetry run python $SCRIPTS_DIR/sl2spacy.py "$sl_file" "$2" "$(wc -l < "$sl_file")"

poetry run python "$SCRIPTS_DIR/sl2spacy.py" "$2/train.sl" "$2"
poetry run python "$SCRIPTS_DIR/sl2spacy.py" "$2/test.sl" "$2"
poetry run python "$SCRIPTS_DIR/sl2spacy.py" "$2/dev.sl" "$2"


