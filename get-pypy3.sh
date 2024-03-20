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
mv -v -- "${pypy}"/bin/pypy3.10 ./pypy3.10
mv -v -- "${pypy}"/bin/libpypy3.10-c.so ./libpypy3.10-c.so
rm -rf -- "${pypy}"

export LD_LIBRARY_PATH="${PWD}:${LD_LIBRARY_PATH-}"

bash
rm -vf ./pypy3.10
rm -vf ./libpypy3.10-c.so
rm -f ./puzzle
