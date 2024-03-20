#!/usr/bin/env bash

set -e

if [ -z "${2}" ]; then
	echo "Usage: "${0}" SIZE CMD ARGS..."
	exit 1
fi

command -v python3 1>/dev/null || { echo "Can't find python3, exiting."; exit 2; }
command -v valgrind 1>/dev/null || { echo "Can't find valgrind, exiting."; exit 3; }
command -v xargs 1>/dev/null || { echo "Can't find xargs, exiting."; exit 4; }
command -v bc 1>/dev/null || { echo "Can't find bc, exiting."; exit 5; }
command -v shasum 1>/dev/null || { echo "Can't find shasum, exiting."; exit 6; } # should be sha1sum by default
command -v wget 1>/dev/null || { echo "Can't find wget, exiting."; exit 7; }

generator="./npuzzle-gen.py"
verifier="./npuzzle-verify.py"

sha1sum_puzzle_gen="$(shasum 2>/dev/null < "${generator}" | cut -f1 -d' ')"
sha1sum_puzzle_verify="$(shasum 2>/dev/null < "${verifier}" | cut -f1 -d' ')"

[ -f "${generator}" ] && [ "${sha1sum_puzzle_gen}" = "3fa00f017bbbb90576861b466bc7dfde06946145" ] || wget -qO "${generator}" 'https://gist.githubusercontent.com/cubernetes/39a9d35a241386f2fb7e6c4f3bdd58d6/raw/a5a8895caf987cb9b465c3b1685f4bd063fdd5fa/npuzzle-gen.py'
[ -f "${verifier}" ] && [ "${sha1sum_puzzle_gen}" = "927044cb9b3bb0b93c283d3a4488b6501ce7a29b" ] || wget -qO "${verifier}" 'https://gist.githubusercontent.com/cubernetes/39a9d35a241386f2fb7e6c4f3bdd58d6/raw/a5a8895caf987cb9b465c3b1685f4bd063fdd5fa/npuzzle-verify.py'
chmod +x "${generator}"
chmod +x "${verifier}"

size="${1}"
shift

result_verifier="$("${generator}" -s "${size}" 1> ./puzzle && ( cat ./puzzle && valgrind -q --tool=massif --massif-out-file=./npuzzle-mem-usage "${@}" < ./puzzle 2> benchmark_stats) | "${verifier}")"
result_massif="$(grep -B3 '=peak$' ./npuzzle-mem-usage | head -n 2 | cut -d= -f2 | xargs | sed 's/ /+/g' | bc | sed 's/\(.\{6\}\)$/.\1/')"

printf '%s, Memory Peak: %s MB\n%s\n' "$(< ./benchmark_stats)" "${result_massif}" "${result_verifier}"

rm -f ./benchmark_stats
rm -f ./npuzzle-mem-usage
rm -f ./puzzle
