#!/usr/bin/env bash

set -euo pipefail

url="https://downloads.python.org/pypy/pypy3.10-v7.3.15-linux64.tar.bz2"
ext=".tar.bz2"
pypy="$(basename -s "${ext}" -- "${url}")"

rm -f -- "${pypy}${ext}"
rm -vf ./pypy3.10
rm -vf ./libpypy3.10-c.so
wget -v "${url}"

tar -xf ./"${pypy}${ext}"
rm -v -- "${pypy}${ext}"
mkdir -pv -- "./pypylib/"
mv -v -- "${pypy}"/bin/pypy3.10 ./pypy3.10
mv -v -- "${pypy}"/bin/libpypy3.10-c.so ./pypylib/libpypy3.10-c.so
mv -v -- "${pypy}"/lib/*.so* ./pypylib/
rm -rf -- "${pypy}"

export LD_LIBRARY_PATH="${LD_LIBRARY_PATH-}:/lib:/lib64:/usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64:${PWD}/pypylib"

bash
rm -vf ./pypy3.10
rm -vf ./libpypy3.10-c.so
rm -f ./puzzle
rm -rvf -- "./pypylib/"
