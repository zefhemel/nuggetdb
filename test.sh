#!/bin/bash

make || exit
cd java-output/bin
java -cp ../lib/mysql-connector.jar:../lib/json.jar:../lib/pil.jar:. Main
cd ../..
