#!/usr/bin/env python3

import sys
import copy
from typing import TextIO

def exit_error(msg: str, exit_code: int) -> None:
    print(f'\033\x5b31m{msg}\033\x5bm', file=sys.stderr, flush=True)
    if exit_code:
        raise SystemExit(exit_code)

def get_line_without_comments(file: TextIO) -> list[str]:
    lines = []
    raw_lines = file.read().strip().splitlines()
    for line in raw_lines:
        line = line.split('#', 1)[0].strip()
        if line:
            lines.append(line)
    return lines

def parse_puzzle_and_solution(file: TextIO) -> tuple[list[list[int]], str]:
    all_lines = get_line_without_comments(file)
    if not all_lines:
        exit_error('No input found', 1)
    size, *lines = all_lines
    *lines, solution_string = lines
    try:
        size = int(size)
    except ValueError:
        exit_error('Can\'t convert size to int', 2)
    if not size:
        exit_error('Size can\'t be zero', 3)
    if len(lines) != size:
        exit_error('Size of input unequals expected size', 4)
    puzzle = []
    for line in lines:
        row = []
        try:
            row = [tile if (tile := int(n)) != 0 else 0 for n in line.split()]
        except ValueError:
            exit_error('exit_error convert input to ints', 5)
        if len(row) != size:
            exit_error('Size of one row unequals expected size', 6)
        puzzle.append(row)
    return puzzle, solution_string

def get_tile_pos(puzzle: list[list[int]], size: int, tile: int) -> tuple[int, int]:
    tile_idx = (-1, -1)
    for r in range(size):
        for c in range(size):
            if puzzle[r][c] == tile:
                tile_idx = (r, c)
    if tile_idx == (-1, -1):
        exit_error(f'Tile "{tile}" is missing.', 7)
    return tile_idx

def print_puzzle(puzzle: list[list[int]], tile: int = -1) -> None:
    size = len(puzzle)
    for i, row in enumerate(puzzle):
        for j, col in enumerate(row):
            if col == tile:
                print(end=f'\033\x5b30;43m{col: >2} \033\x5bm')
            elif col == i * size + j + 1 and col < tile:
                print(end=f'\033\x5b30;42m{col: >2} \033\x5bm')
            elif col == 0:
                print(end=f'\033\x5b30;41m{col: >2} \033\x5bm')
            else:
                print(end=f'{col: >2} ')
        print()
    print()

def move(puzzle: list[list[int]], size: int, moves: str) -> None:
    global original_puzzle
    r, c = get_tile_pos(puzzle, size, 0)
    for move in moves:
        try:
            if move == 'd':
                puzzle[r][c], puzzle[r+1][c] = puzzle[r+1][c], puzzle[r][c]
                r += 1
            elif move == 'u':
                if r-1 < 0: raise IndexError(f'negative index: {r-1}')
                puzzle[r][c], puzzle[r-1][c] = puzzle[r-1][c], puzzle[r][c]
                r -= 1
            elif move == 'r':
                puzzle[r][c], puzzle[r][c+1] = puzzle[r][c+1], puzzle[r][c]
                c += 1
            elif move == 'l':
                if c-1 < 0: raise IndexError(f'negative index: {c-1}')
                puzzle[r][c], puzzle[r][c-1] = puzzle[r][c-1], puzzle[r][c]
                c -= 1
            else:
                exit_error(f'Unknown move "{move}".', 8)

        except IndexError as err:
            print_puzzle(original_puzzle)
            exit_error(f'{move=}, {r=}, {c=}, {err=}\n', 9)

def puzzle_solved(puzzle: list[list[int]], size: int) -> bool:
    expected_tile = 1
    for row in puzzle:
        for tile in row:
            if tile == 0:
                if expected_tile != size ** 2:
                    return False
            elif tile != expected_tile:
                return False
            expected_tile += 1
    return True

def verify_puzzle(puzzle: list[list[int]], solution_str: str) -> bool:
    size = len(puzzle)
    move(puzzle, size, solution_str)
    return puzzle_solved(puzzle, size)

if __name__ == "__main__":
    global original_puzzle
    puzzle, solution_string = parse_puzzle_and_solution(open(0))
    original_puzzle = copy.deepcopy(puzzle)
    if verify_puzzle(puzzle, solution_string):
        print('\033\x5b32mOK\033\x5bm')
    else:
        print('\033\x5b31mKO\033\x5bm')
        print('Input Puzzle')
        print_puzzle(original_puzzle)
        print('Output Puzzle')
        print_puzzle(puzzle)
