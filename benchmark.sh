#!/usr/bin/env bash

set -e

if [ -z "${2}" ]; then
	echo "Usage: "${0}" SIZE CMD ARGS..."
	exit 1
fi

size="${1}"
shift

result_verifier="$(./npuzzle-gen.py -s "${size}" 1> ./puzzle && ( cat ./puzzle && valgrind -q --tool=massif --massif-out-file=./npuzzle-mem-usage "${@}" < ./puzzle 2> benchmark_stats) | ./pypy3.10 ./npuzzle-verify.py)"
result_massif="$(grep -B3 '=peak$' ./npuzzle-mem-usage | head -2 | cut -d= -f2 | xargs | sed 's/ /+/g' | bc | sed 's/\(.\{6\}\)$/.\1/')"
printf '%s, Memory Peak: %s MB\n%s\n' "$(< ./benchmark_stats)" "${result_massif}" "${result_verifier}"
rm -f ./benchmark_stats
rm -f ./npuzzle-mem-usage
rm -f ./puzzle
