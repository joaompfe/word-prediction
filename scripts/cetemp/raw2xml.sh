#!/bin/bash

if [[ ! -f $1 ]]; then
	echo "$1 is not a file"
    exit 1  
fi
if [[ ! -f $2 ]]; then
	touch "$2"
fi

sed -E	-e '$a</data>' \
		-e '1s/^/<data> /' \
		-e '/^[[:space:]]*$/d' \
		-e "s/<ext\sn=([0-9]+)\ssec=([a-z-]+)\ssem=([0-9a-z-]+)>/<ext n=\"\1\" sec=\"\2\" sem=\"\3\">/" \
		-e 's/<marca\snum=\"?.+\"?>//' \
		-e 's/<s\stipo=([a-z]+)>/<s tipo=\"\1\">/' "$1" > "$2"
