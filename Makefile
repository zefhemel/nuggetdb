PILJAR=/Users/zef/svn/pil/src/lib/pil.jar

all:
	rm -rf java-output
	mkdir -p java-output/src
	pilc -i test.pil -d java-output/src
	cp -r java-support/* java-output/
	cp $(PILJAR) java-output/lib
	cd java-output; ant

run:
