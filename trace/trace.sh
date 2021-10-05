#! /bin/bash

for i in $(seq $1 $2); do 
	echo $i
	sed 's/\[/(/g; s/\]/)/g' out$i > out-$i
	echo $i >> rez
	mv out-$i inctmp
	../form/form trace.frm > /dev/null
	mv inctmp out-$i 
done