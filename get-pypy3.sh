#!/usr/bin/env bash

set -euo pipefail

url="https://downloads.python.org/pypy/pypy3.10-v7.3.15-linux64.tar.bz2"
ext=".tar.bz2"
pypy="$(basename -s "${ext}" -- "${url}")"

echo "Hello! Please be patient, the downloading and extraction of pypy might take a few seconds."
rm -f -- "${pypy}${ext}"
rm -f ./pypy3.10
rm -f ./libpypy3.10-c.so
wget --show-progress -q "${url}"

tar -xf ./"${pypy}${ext}"
rm -- "${pypy}${ext}"
mkdir -p -- "./pypylib/"
mv -- "${pypy}"/bin/pypy3.10 ./pypy3.10
mv -- "${pypy}"/bin/libpypy3.10-c.so ./pypylib/libpypy3.10-c.so
mv -- "${pypy}"/lib/*.so* ./pypylib/
rm -rf -- "${pypy}"

export LD_LIBRARY_PATH="${LD_LIBRARY_PATH-}:/lib:/lib64:/usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64:${PWD}/pypylib"

function cleanup () {
	rm -f ./pypy3.10
	rm -f ./libpypy3.10-c.so
	rm -f ./puzzle
	rm -rf -- "./pypylib/"
}

trap cleanup EXIT

echo "Done! Starting a child shell (for the correct environment). When you exit this shell, pypy will be deleted from the current directory."
bash
