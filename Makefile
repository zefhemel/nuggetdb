PILJAR=/Users/zef/svn/pil/src/lib/pil.jar

all: clean
	mkdir -p java-output/src
	pilc -i test.pil -d java-output/src --gen-external-classinfos
	cp -r java-support/* java-output/
	cp $(PILJAR) java-output/lib
	cd java-output; ant

clean:
	rm -f *.pil.h nuggetdb/*.pil.h
	rm -rf java-output
