#!/usr/bin/env bash

set -euo pipefail

url="https://downloads.python.org/pypy/pypy3.10-v7.3.15-linux64.tar.bz2"
ext=".tar.bz2"
pypy="$(basename -s "${ext}" -- "${url}")"

if [ ! -d "${pypy}" ]; then
	rm -rf -- "${pypy}"
	echo "Hello! Please be patient, the downloading and extraction of pypy might take a few seconds."
	wget --show-progress -q "${url}"
	tar -xf ./"${pypy}${ext}"
	rm -- "${pypy}${ext}"
fi

ln -sf "${pypy}/bin/pypy3.10" ./pypy3.10
