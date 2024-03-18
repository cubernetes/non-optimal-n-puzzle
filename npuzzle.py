#!/usr/bin/env python3

import os
import sys
import time
import timeit
import typing
import inspect

def move_empty(dir: str, puzzle: list[list[int]]) -> list[str]:
    global empty_idx, tile_idx
    r, c = empty_idx
    if dir == 'd':
        puzzle[r][c], puzzle[r+1][c] = puzzle[r+1][c], puzzle[r][c]
        empty_idx[0] += 1
    elif dir == 'u':
        puzzle[r][c], puzzle[r-1][c] = puzzle[r-1][c], puzzle[r][c]
        empty_idx[0] -= 1
    elif dir == 'r':
        puzzle[r][c], puzzle[r][c+1] = puzzle[r][c+1], puzzle[r][c]
        empty_idx[1] += 1
    elif dir == 'l':
        puzzle[r][c], puzzle[r][c-1] = puzzle[r][c-1], puzzle[r][c]
        empty_idx[1] -= 1
    print_puzzle(puzzle)
    # time.sleep(.1)
    return [dir]

def move_tile_to_line(line: int, tile: int, puzzle: list[list[int]]) -> list[str]:
    global empty_idx, tile_idx
    insts = []

    if tile_idx[0] < len(puzzle) - 1:
        off = 1
    else:
        off = -1
    while empty_idx[0] < tile_idx[0] + off:
        insts += move_empty('d', puzzle)
    while empty_idx[0] > tile_idx[0] + off:
        insts += move_empty('u', puzzle)
    while empty_idx[1] < tile_idx[1]:
        insts += move_empty('r', puzzle)
    while empty_idx[1] > tile_idx[1]:
        insts += move_empty('l', puzzle)
    if off == -1:
        insts += move_empty('d', puzzle)
        tile_idx[0] -= 1

    diff = tile_idx[0] - line
    for i in range(diff):
        if tile_idx[1] < tile - 1 - line * len(puzzle):
            insts += move_empty('r', puzzle)
            insts += move_empty('u', puzzle)
            insts += move_empty('u', puzzle)
            insts += move_empty('l', puzzle)
        else:
            insts += move_empty('l', puzzle)
            insts += move_empty('u', puzzle)
            insts += move_empty('u', puzzle)
            insts += move_empty('r', puzzle)
        insts += move_empty('d', puzzle)

    return insts

    if tile_idx[0] < line - 1:
        print(f'Tile {tile} is in line {tile_idx[0]} (too high)')
        raise SystemExit(9)
    elif tile_idx[0] == line - 1:
        while empty_idx[0] < line:
            insts += move_empty('d', puzzle)
        while empty_idx[0] > line:
            insts += move_empty('u', puzzle)
        while empty_idx[1] < tile_idx[1]:
            insts += move_empty('r', puzzle)
        while empty_idx[1] > tile_idx[1]:
            insts += move_empty('l', puzzle)
        insts += move_empty('u', puzzle)
        if tile_idx[1] == len(puzzle) - 1:
            insts += move_empty('l', puzzle)
            insts += move_empty('d', puzzle)
            insts += move_empty('d', puzzle)
            insts += move_empty('r', puzzle)
        else:
            insts += move_empty('r', puzzle)
            insts += move_empty('d', puzzle)
            insts += move_empty('d', puzzle)
            insts += move_empty('l', puzzle)
        return insts
    elif tile_idx[0] == line:
        while empty_idx[0] < tile_idx[0] + 1:
            insts += move_empty('d', puzzle)
        while empty_idx[0] > tile_idx[0] + 1:
            insts += move_empty('u', puzzle)
        while empty_idx[1] < tile_idx[1]:
            insts += move_empty('r', puzzle)
        while empty_idx[1] > tile_idx[1]:
            insts += move_empty('l', puzzle)
        return insts

    if empty_idx[1] == tile_idx[1] and empty_idx[0] > tile_idx[0]:
        if empty_idx[1] == len(puzzle) - 1:
            insts += move_empty('l', puzzle)
        else:
            insts += move_empty('r', puzzle)

    if tile_idx[1] < tile - 1 - line * len(puzzle):
        if empty_idx[1] < len(puzzle) - 1:
            insts += move_empty('r', puzzle)
        while empty_idx[0] < tile_idx[0]:
            insts += move_empty('d', puzzle)
        while empty_idx[0] > tile_idx[0]:
            insts += move_empty('u', puzzle)
        while empty_idx[1] < tile_idx[1] + 1:
            insts += move_empty('r', puzzle)
        while empty_idx[1] > tile_idx[1] + 1:
            insts += move_empty('l', puzzle)
        diff = (tile - 1 - line * len(puzzle)) - tile_idx[1]
        for i in range(diff):
            insts += move_empty('l', puzzle)
            tile_idx[1] += 1
            if tile_idx[0] == len(puzzle) - 1:
                insts += move_empty('u', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('d', puzzle)
            else:
                insts += move_empty('d', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('u', puzzle)

    while empty_idx[0] < tile_idx[0] - 1:
        insts += move_empty('d', puzzle)
    while empty_idx[0] > tile_idx[0] - 1:
        insts += move_empty('u', puzzle)

    while empty_idx[1] < tile_idx[1]:
        insts += move_empty('r', puzzle)
    while empty_idx[1] > tile_idx[1]:
        insts += move_empty('l', puzzle)

    diff = tile_idx[0] - line
    for i in range(diff):
        insts += move_empty('d', puzzle)
        if i < diff - 1:
            if tile_idx[1] == tile - 1 - line * len(puzzle):
                insts += move_empty('r', puzzle)
                insts += move_empty('u', puzzle)
                insts += move_empty('u', puzzle)
                insts += move_empty('l', puzzle)
            else:
                insts += move_empty('l', puzzle)
                insts += move_empty('u', puzzle)
                insts += move_empty('u', puzzle)
                insts += move_empty('r', puzzle)

    return insts

def move_tile_left(line: int, tile: int, puzzle: list[list[int]]) -> list[str]:
    global empty_idx, tile_idx
    diff = tile_idx[1] - (tile - line * len(puzzle) - 1)
    insts = []
    if diff > 0:
        insts += move_empty('l', puzzle)
        insts += move_empty('u', puzzle)
        for i in range(diff):
            insts += move_empty('r', puzzle)
            if i < diff - 1:
                insts += move_empty('d', puzzle)
                insts += move_empty('l', puzzle)
                insts += move_empty('l', puzzle)
                insts += move_empty('u', puzzle)
            else:
                insts += move_empty('d', puzzle)
                insts += move_empty('l', puzzle)
    elif diff < 0:
        diff = abs(diff)
        insts += move_empty('r', puzzle)
        insts += move_empty('u', puzzle)
        for i in range(diff):
            insts += move_empty('l', puzzle)
            if i < diff - 1:
                insts += move_empty('d', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('u', puzzle)
            else:
                insts += move_empty('d', puzzle)
                insts += move_empty('r', puzzle)
    return insts

def move_tile_very_right(line: int, tile: int, puzzle: list[list[int]]) -> list[str]:
    global empty_idx, tile_idx
    diff = tile_idx[1] - (tile - line * len(puzzle) - 1)
    insts = []
    if diff > 0:
        print(f"Tile can't be outside square, something's off ({tile_idx=}, {tile - line * len(puzzle) - 1=}")
        raise SystemExit(11)
    elif diff < 0:
        diff = abs(diff)
        insts += move_empty('r', puzzle)
        insts += move_empty('u', puzzle)
        for i in range(diff):
            insts += move_empty('l', puzzle)
            if i < diff - 1:
                insts += move_empty('d', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('r', puzzle)
                insts += move_empty('u', puzzle)
            else:
                insts += move_empty('d', puzzle)
                insts += move_empty('r', puzzle)
    return insts

def solve_n_minus_2_line(line: int, puzzle: list[list[int]]) -> list[str]:
    global empty_idx, tile_idx
    insts = []
    for i in range(1, len(puzzle)):
        print(f'Solving tile {i + line * len(puzzle)}')
        get_idxs(i + line * len(puzzle))
        if tile_idx[0] * len(puzzle) + tile_idx[1] == i + line * len(puzzle) - 1:
            continue
        insts += move_tile_to_line(line, i + line * len(puzzle), puzzle)
        insts += move_tile_left(line, i + line * len(puzzle), puzzle)
    return insts

def solve_last_tile_in_line(line: int, puzzle: list[list[int]]) -> list[str]:
    global empty_idx, tile_idx
    insts = []
    insts += move_empty('r', puzzle)
    insts += move_empty('u', puzzle)
    insts += move_empty('l', puzzle)
    insts += move_empty('d', puzzle)
    get_idxs(len(puzzle) + line * len(puzzle))
    if tile_idx[0] == empty_idx[0] - 1 and tile_idx[1] == empty_idx[1]:
        print('Edge case! Last tile in line was at unfortunate position')
        raise SystemExit(10)
    print('moving tile to line')
    insts += move_tile_to_line(line + 1, len(puzzle) + line * len(puzzle), puzzle)
    print('moving tile very right')
    insts += move_tile_very_right(line, len(puzzle) + line * len(puzzle), puzzle)
    insts += move_empty('l', puzzle)
    insts += move_empty('u', puzzle)
    insts += move_empty('u', puzzle)
    insts += move_empty('r', puzzle)
    insts += move_empty('d', puzzle)
    return insts

def solve_line(line: int, puzzle: list[list[int]]) -> list[str]:
    insts = solve_n_minus_2_line(line, puzzle)
    insts += solve_last_tile_in_line(line, puzzle)
    return insts

def solve_n_minus_2(puzzle: list[list[int]]) -> list[str]:
    insts = []
    for line in range(len(puzzle) - 2):
        insts += solve_line(line, puzzle)
    return insts

def solve_last_2(puzzle: list[list[int]]) -> list[str]:
    pass

def solve(puzzle: list[list[int]]) -> list[str]:
    insts = solve_n_minus_2(puzzle)
    # insts += solve_last_2(puzzle)
    return insts

if os.environ.get('DEBUG') == '1':
    def debug(function):
        def inner(*args, **kwargs):
            print(f'Calling {function.__name__}')
            return function(*args, **kwargs)
        return inner
else:
    def debug(function):
        return function

class Puzzle:
    @debug
    def __init__(self,
            file: typing.TextIO,
            *,
            print_after_move: bool = False,
            debug: bool = False,
            delay: float = .5,
        ):
        """Initialize puzzle, determine solvability and find empty tile
        Takes O(n**4) (self._is_solvable()).
        """
        self.puzzle: list[list[int]]
        self.is_solvable: bool
        self.size: int
        self.empty_row: int
        self.empty_col: int
        self.moves: list[str]

        self.file = file
        self.print_after_move = print_after_move
        self.debug = debug
        self.delay = delay
        self.puzzle = self._parse_puzzle()
        self.is_solvable = self._is_solvable()
        self.size = len(self.puzzle)
        empty_pos: tuple[int, int] = self._get_tile_pos(0)
        self.empty_row = empty_pos[0]
        self.empty_col = empty_pos[1]
        self.moves = []

        if self.print_after_move:
            print('\033\x5b30;42mInitial puzzle:\033\x5bm')
            self.print_puzzle()

    @debug
    def _get_line_without_comments(self) -> list[str]:
        """Return list of lines with comments removed.
        Takes at least O(n**2).
        """
        lines = []
        raw_lines = self.file.read().strip().splitlines()
        for line in raw_lines:
            line = line.split('#', 1)[0].strip()
            if line:
                lines.append(line)
        return lines

    @debug
    def _parse_puzzle(self) -> list[list[int]]:
        """Return a 2-dimensional integer array with the same number of rows
        as columns, representing the N-puzzle. One entry will be 0, representing
        the empty tile.
        Takes at least O(n**2).
        """
        all_lines = self._get_line_without_comments()
        if not all_lines:
            self.error('No input found', 1)
        size, *lines = all_lines
        try:
            size = int(size)
        except ValueError:
            self.error('Can\'t convert size to int', 2)
        if not size:
            self.error('Size can\'t be zero', 3)
        if len(lines) != size:
            self.error('Size of input unequals expected size', 4)
        puzzle = []
        for line in lines:
            row = []
            try:
                row = [tile if (tile := int(n)) != 0 else 0 for n in line.split()]
            except ValueError:
                self.error('Error convert input to ints', 5)
            if len(row) != size:
                self.error('Size of one row unequals expected size', 6)
            puzzle.append(row)
        return puzzle

    @debug
    def _is_solvable(self) -> bool:
        """Determine if the puzzle can be turned back to the standard
        configuration just by doing swaps with the empty tile.
        Takes (n**4). Can be improved to O(n**3 * log(n)).
        """
        flat_puzzle = []
        for row in self.puzzle:
            for c in row:
                flat_puzzle.append(c)
        n_inversions = 0
        for i in range(0, len(flat_puzzle)):
            for j in range(i + 1, len(flat_puzzle)):
                if flat_puzzle[i] > flat_puzzle[j]:
                    n_inversions += 1
        empty_idx = flat_puzzle.index(0)
        row = empty_idx % len(self.puzzle)
        col = empty_idx // len(self.puzzle)
        return (row + col + n_inversions) % 2 == 1

    @debug
    def _get_tile_pos(self, tile: int) -> tuple[int, int]:
        """Linearly search for a tile.
        Takes O(n**2).
        """
        tile_idx = (-1, -1)
        for r in range(self.size):
            for c in range(self.size):
                if self.puzzle[r][c] == tile:
                    tile_idx = (r, c)
        if tile_idx == (-1, -1):
            self.error(f'Tile "{tile}" is missing.', 7)
        return tile_idx

    @debug
    def print_puzzle(self, tile: int = -1) -> None:
        """Print puzzle as a 2d square and color the empty square red.
        Also color the :tile green if provided. Empty square will be green
        if tile == 0.
        Takes O(n**2).
        """
        for row in self.puzzle:
            for col in row:
                if col == tile:
                    print(end=f'\033\x5b30;42m{col: >2} \033\x5bm')
                elif col != 0:
                    print(end=f'{col: >2} ')
                else:
                    print(end=f'\033\x5b30;41m{col: >2} \033\x5bm')
            print()
        print()

    @debug
    def print_moves(self) -> None:
        """Print list of moves as one string
        Takes O(n**2).
        """
        if self.moves:
            print(''.join(self.moves))
        else:
            print('Empty list of moves')

    @debug
    def error(self, msg: str, exit_code: int) -> None:
        """Print error :msg to standard output and exit process with non-zero
        :exit_code. If exit_code is 0, do not exit.
        """
        print(f'\033\x5b31m{msg}\033\x5bm', file=sys.stderr, flush=True)
        if exit_code:
            raise SystemExit(exit_code)

    @debug
    def move(self, moves: str, tile: int = -1) -> None:
        """Perform moves (swaps with the emtpy tile) sequentially, provided as each character of :moves.
        Takes O(moves).
        """
        r, c = self.empty_row, self.empty_col
        for move in moves:
            time.sleep(self.delay)
            try:
                if move == 'd':
                    self.puzzle[r][c], self.puzzle[r+1][c] = self.puzzle[r+1][c], self.puzzle[r][c]
                    self.empty_row = r = r + 1
                elif move == 'u':
                    if r-1 < 0: raise IndexError(f'negative index: {r-1}')
                    self.puzzle[r][c], self.puzzle[r-1][c] = self.puzzle[r-1][c], self.puzzle[r][c]
                    self.empty_row = r = r - 1
                elif move == 'r':
                    self.puzzle[r][c], self.puzzle[r][c+1] = self.puzzle[r][c+1], self.puzzle[r][c]
                    self.empty_col = c = c + 1
                elif move == 'l':
                    if c-1 < 0: raise IndexError(f'negative index: {c-1}')
                    self.puzzle[r][c], self.puzzle[r][c-1] = self.puzzle[r][c-1], self.puzzle[r][c]
                    self.empty_col = c = c - 1
                else:
                    self.error(f'Unknown move "{move}".', 8)
                self.moves.append(move)
                if self.print_after_move:
                    self.print_puzzle(tile=tile)
            except IndexError as err:
                self.error(f'{move=}, {r=}, {c=}, {err=}\n', 9)

    @debug
    def focus_tile_top(self, real_tile: list[int]) -> None:
        """Move the empty tile such that it is immediately above the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it is below a solved tile.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = real_tile
        tile = self.puzzle[tile_real_row][tile_real_col]
        if tile_real_row == self.size - 1:
            while self.empty_row < tile_real_row - 1:
                self.move('d', tile)
            while self.empty_row > tile_real_row - 1:
                self.move('u', tile)
            while self.empty_col < tile_real_col:
                self.move('r', tile)
            while self.empty_col > tile_real_col:
                self.move('l', tile)
        else:
            self.focus_tile_bottom(real_tile)
            self.move('u', tile)
            real_tile[0] += 1

    @debug
    def focus_tile_bottom(self, real_tile: list[int]) -> None:
        """Move the empty tile such that it is immediately below the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it is already at the bottom.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = real_tile
        tile = self.puzzle[tile_real_row][tile_real_col]
        if self.empty_col == tile_real_col and self.empty_row < tile_real_row:
            one_off = 0
            real_tile[0] -= 1
        else:
            one_off = 1
        while self.empty_row < tile_real_row + one_off:
            self.move('d', tile)
        while self.empty_row > tile_real_row + one_off:
            self.move('u', tile)
        while self.empty_col < tile_real_col:
            self.move('r', tile)
        while self.empty_col > tile_real_col:
            self.move('l', tile)

    @debug
    def focus_tile_left(self, real_tile: list[int]) -> None:
        """Move the empty tile such that it is immediately left to the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it is all the way to the left.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = real_tile
        tile = self.puzzle[tile_real_row][tile_real_col]
        if tile_real_col == self.size - 1:
            while self.empty_col < tile_real_col - 1:
                self.move('r', tile)
            while self.empty_col > tile_real_col - 1:
                self.move('l', tile)
            while self.empty_row < tile_real_row:
                self.move('d', tile)
            while self.empty_row > tile_real_row:
                self.move('u', tile)
        else:
            self.focus_tile_right(real_tile)
            self.move('l', tile)
            real_tile[1] += 1

    @debug
    def focus_tile_right(self, real_tile: list[int]) -> None:
        """Move the empty tile such that it is immediately right to the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it all the way to the right.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = real_tile
        tile = self.puzzle[tile_real_row][tile_real_col]
        if self.empty_row == tile_real_row and self.empty_col < tile_real_col:
            one_off = 0
            real_tile[1] -= 1
        else:
            one_off = 1
        while self.empty_col < tile_real_col + one_off:
            self.move('r', tile)
        while self.empty_col > tile_real_col + one_off:
            self.move('l', tile)
        while self.empty_row < tile_real_row:
            self.move('d', tile)
        while self.empty_row > tile_real_row:
            self.move('u', tile)

    # def tile_solved(self, tile: int) -> bool:
    #     """Return True if the :tile is already in its correct position.
    #     No requirements.
    #     """
    #     if tile == 0:
    #         tile_idx = self.size ** 2 - 1
    #     else:
    #         tile_idx = tile - 1
    #     r, c = divmod(tile_idx, self.size)
    #     return self.puzzle[r][c] == tile

    @debug
    def move_horizontally_using_bottom(self, tile_real_row: int, tile_real_col: int, tile_correct_row: int, tile_correct_col: int) -> bool:
        """Return True if the immediate top position of the tile to be moved
        is ideal/necessary for horizontal movement, False otherwise.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        if tile_real_row == self.size - 1:
            return False
        elif tile_real_row == tile_correct_row:
            return True
        elif tile_real_row == tile_correct_row + 1:
            if tile_real_col < tile_correct_col:
                return True
            return self.empty_row >= tile_real_row
        return self.empty_row >= tile_real_row

    @debug
    def move_vertically_using_right(self, _tile_real_row: int, tile_real_col: int, _tile_correct_row: int, _tile_correct_col: int) -> bool:
        """Return True if the immediate right position of the tile to be moved
        is ideal/necessary for vertical movement, False otherwise.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted and
        (requires tile to be aligned horizontally to work optimally).
        """
        if tile_real_col == self.size - 1:
            return False
        return True

    @debug
    def align_tile_horizontally(self, tile: int, real_tile: list[int], tile_correct_row: int, tile_correct_col: int, repositioning_moves: str) -> None:
        """Move tile left or right until it reaches :tile_correct_col
        """
        tile_real_row, tile_real_col = real_tile
        first = True
        while tile_real_col < tile_correct_col:
            if first:
                self.focus_tile_right(real_tile)
                first = False
            else:
                self.move(repositioning_moves, tile)
            self.move('l', tile)
            tile_real_col = real_tile[1] = real_tile[1] + 1
        while tile_real_col > tile_correct_col:
            if first:
                self.focus_tile_left(real_tile)
                first = False
            else:
                self.move(repositioning_moves, tile)
            self.move('r', tile)
            tile_real_col = real_tile[1] = real_tile[1] - 1

    @debug
    def align_tile_vertically(self, tile: int, real_tile: list[int], tile_correct_row: int, tile_correct_col: int, repositioning_moves: str) -> None:
        """Move tile top or down until it reaches :tile_correct_row
        """
        tile_real_row, tile_real_col = real_tile
        first = True
        while tile_real_row < tile_correct_row:
            if first:
                self.focus_tile_bottom(real_tile)
                first = False
            else:
                self.move(repositioning_moves, tile)
            self.move('u', tile)
            tile_real_row = real_tile[0] = real_tile[0] + 1
        while tile_real_row > tile_correct_row:
            if first:
                self.focus_tile_top(real_tile)
                first = False
            else:
                self.move(repositioning_moves, tile)
            self.move('d', tile)
            tile_real_row = real_tile[0] = real_tile[0] - 1

    @debug
    def get_horizontal_repositioning_moves(self, real_tile: list[int], tile_correct_row: int, tile_correct_col: int) -> str:
        """Return the needed repositioning moves after a tile has been moved
        horizontally to make the moving of the tile repeatable.
        """
        tile_real_row, tile_real_col = real_tile
        if self.move_horizontally_using_bottom(tile_real_row, tile_real_col, tile_correct_row, tile_correct_col):
            if tile_real_col < tile_correct_col:
                repositioning_moves = 'drru'
            else:
                repositioning_moves = 'dllu'
        else:
            if tile_real_col < tile_correct_col:
                repositioning_moves = 'urrd'
            else:
                repositioning_moves = 'ulld'
        return repositioning_moves

    @debug
    def get_vertical_repositioning_moves(self, real_tile: list[int], tile_correct_row: int, tile_correct_col: int) -> str:
        """Return the needed repositioning moves after a tile has been moved
        vertically to make the moving of the tile repeatable.
        """
        tile_real_row, tile_real_col = real_tile
        if self.move_vertically_using_right(tile_real_row, tile_real_col, tile_correct_row, tile_correct_col):
            if tile_real_row < tile_correct_row:
                repositioning_moves = 'rddl'
            else:
                repositioning_moves = 'ruul'
        else:
            if tile_real_row < tile_correct_row:
                repositioning_moves = 'lddr'
            else:
                repositioning_moves = 'luur'
        return repositioning_moves

    @debug
    def solve_row_n_minus_2_tiles(self, row: int) -> None:
        """Solve first n-2 tiles of a particular :row.
        Requires that all previous rows are completely solved.
        """
        first_tile = row * self.size + 1
        last_tile = first_tile + self.size - 3
        for tile in range(first_tile, last_tile + 1):
            real_tile = list(self._get_tile_pos(tile))
            tile_idx = tile - 1 if tile != 0 else self.size ** 2 - 1
            tile_correct_row, tile_correct_col = divmod(tile_idx, self.size)

            repositioning_moves_horizontal = self.get_horizontal_repositioning_moves(real_tile, tile_correct_row, tile_correct_col)
            self.align_tile_horizontally(tile, real_tile, tile_correct_row, tile_correct_col, repositioning_moves_horizontal)
            repositioning_moves_vertical = self.get_vertical_repositioning_moves(real_tile, tile_correct_row, tile_correct_col)
            self.align_tile_vertically(tile, real_tile, tile_correct_row, tile_correct_col, repositioning_moves_vertical)

    @debug
    def solve_row_last_2_tiles(self, row: int) -> None:
        """Solve last 2 tiles of a particular :row.
        Requires that all previous tiles in that row are solved.
        """

    @debug
    def solve_n_minus_2_rows(self) -> None:
        """Solve first n-2 rows of the puzzle.
        No additional requirements.
        """
        for row in range(self.size - 2):
            self.solve_row_n_minus_2_tiles(row)
            self.solve_row_last_2_tiles(row)

    @debug
    def solve_last_2_rows_col(self, col: int) -> None:
        """Solve a particular :col from the last 2 rows.
        Requires that all previous columns in the last 2 rows are solved.
        """

    @debug
    def solve_last_2_rows_n_minus_2_cols(self) -> None:
        """Solve the first n-2 columns of the last 2 rows.
        Requires that all previous rows are solved.
        """
        for col in range(self.size - 2):
            self.solve_last_2_rows_col(col)

    @debug
    def solve_last_4_tiles(self) -> None:
        """Solve bottom right 4 tiles. If not self.is_solvable, then this step
        will fail.
        Requires that all tiles of the puzzle are solved, except these last 4.
        """

    @debug
    def solve_last_2_rows(self) -> None:
        """Solve last two rows of the puzzle.
        Requires that all previous rows are solved.
        """
        self.solve_last_2_rows_n_minus_2_cols()
        self.solve_last_4_tiles()

    @debug
    def solve(self) -> None:
        """Turn the puzzle back to its standard configuration and save the moves
        in self.moves
        Takes probably at least O(n**3) multiplied by some big constant, or more.
        Requires that the puzzle is solvable.
        """
        if not puzzle.is_solvable:
            puzzle.error('Puzzle not solvable', 0)
            return
        self.solve_n_minus_2_rows()
        self.solve_last_2_rows()

if __name__ == '__main__':
    puzzle = Puzzle(open(0), print_after_move=False, debug=False, delay=.1)
    elapsed_seconds = timeit.timeit('puzzle.solve()', globals=globals(), number=1)
    print(f'Elapsed seconds: {elapsed_seconds:.6f}')
    print('Solution:')
    puzzle.print_moves()
