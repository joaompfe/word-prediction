#!/bin/bash

if [[ ! -f $1 ]]; then
	echo "$1 is not a file"
    exit 1  
fi
if [[ ! -f $2 ]]; then
	touch $2 
fi

cp $1 $2


perl -i -pe 's/^([^<].*)/{\n\"orth\":\"\1\"\n}/igm' $2
perl -i -pe "s/<ext\sn=\"([0-9]+)\"[^>]*>/{\n\"id\":\1,\n\"paragraphs\":\[/ig;" \
	 	-pe "s/<\/ext>/\]}/ig;" \
		-pe "s/<s(?:\stipo=[a-z]+)?>/{\"tokens\":\[/igs;" \
		-pe "s/<\/s>/\]}/igs;" \
		-pe "s/<p>/{\"sentences\":\[/igs;" \
		-pe "s/<\/p>/\]}/igs;" \
		-pe "s/<data>/\[/i;" \
		-pe "s/<\/data>/\]/i;" \
		$2
		
sed -i -n '1,/<t>/p;/<\/t>/,$p' $2
sed -i '/<t>/,/<\/t>/d' $2

cp $2 "$2.tmp"
perl tmp.pl "$2.tmp" $2
rm  "$2.tmp"
