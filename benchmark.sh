#!/usr/bin/env bash

if [ -z "${1}" ]; then
	echo "Usage: bench SIZE"
	exit 1
fi
./npuzzle-gen.py -s "${1}" 1> ./puzzle && ( cat ./puzzle && ./pypy3.10 --jit vec=1 ./npuzzle.py < ./puzzle ) | ./pypy3.10 ./npuzzle-verify.py
