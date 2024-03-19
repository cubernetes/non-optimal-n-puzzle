#!/usr/bin/env python3

import sys
import time
import timeit
import typing

class Puzzle:
    def __init__(self,
            file: typing.TextIO,
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
        self.puzzle = self._parse_puzzle()
        self.size = len(self.puzzle)
        self.is_solvable = self._is_solvable()
        empty_pos: tuple[int, int] = self._get_tile_pos(0)
        self.empty_row = empty_pos[0]
        self.empty_col = empty_pos[1]
        self.moves = []

        # print('\033\x5b30;42mInitial puzzle:\033\x5bm')
        # self.print_puzzle()

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

    def _is_solvable(self) -> bool:
        """Determine if the puzzle can be turned back to the standard
        configuration just by doing swaps with the empty tile.
        Takes (n**4). Can be improved to O(n**3 * log(n)).
        """
        flat_puzzle = []
        for row in self.puzzle:
            for c in row:
                if c != 0:
                    flat_puzzle.append(c)
                else: # interpret the empty tile (0) as having the square value
                      # this way, number of inversions is 0 for the solved state
                    flat_puzzle.append(self.size ** 2)
        empty_idx = flat_puzzle.index(self.size ** 2)
        row = empty_idx // self.size
        col = empty_idx % self.size

        n_inversions = 0
        for i in range(0, len(flat_puzzle)):
            for j in range(i + 1, len(flat_puzzle)):
                if flat_puzzle[i] > flat_puzzle[j]:
                    n_inversions += 1
        manhatten_to_bottom_right = (self.size - row - 1) + (self.size - col - 1)
        puzzle_parity = (manhatten_to_bottom_right + n_inversions) % 2
        return puzzle_parity == 0

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

    def print_puzzle(self, tile: int = -1) -> None:
        """Print puzzle as a 2d square and color the empty square red.
        Also color the :tile green if provided. Empty square will be green
        if tile == 0.
        Takes O(n**2).
        """
        # print('\033\x5bH\033\x5b2J\033\x5b3J')
        time.sleep(0.5)
        for i, row in enumerate(self.puzzle):
            for j, col in enumerate(row):
                if col == tile:
                    print(end=f'\033\x5b30;43m{col: >2} \033\x5bm')
                elif col == i * self.size + j + 1 and col < tile:
                    print(end=f'\033\x5b30;42m{col: >2} \033\x5bm')
                elif col == 0:
                    print(end=f'\033\x5b30;41m{col: >2} \033\x5bm')
                else:
                    print(end=f'{col: >2} ')
            print()
        print()

    def print_moves(self) -> None:
        """Print list of moves as one string
        Takes O(n**2).
        """
        if self.moves:
            print(''.join(self.moves))
        else:
            print('Empty list of moves')

    def error(self, msg: str, exit_code: int) -> None:
        """Print error :msg to standard output and exit process with non-zero
        :exit_code. If exit_code is 0, do not exit.
        """
        print(f'\033\x5b31m{msg}\033\x5bm', file=sys.stderr, flush=True)
        if exit_code:
            raise SystemExit(exit_code)

    def move(self, moves: str) -> None:
        """Perform moves (swaps with the emtpy tile) sequentially, provided as each character of :moves.
        Takes O(moves).
        """
        for move in moves:
            if move == 'd':
                self.puzzle[self.empty_row][self.empty_col], self.puzzle[self.empty_row+1][self.empty_col] = self.puzzle[self.empty_row+1][self.empty_col], self.puzzle[self.empty_row][self.empty_col]
                self.empty_row += 1
            elif move == 'u':
                self.puzzle[self.empty_row][self.empty_col], self.puzzle[self.empty_row-1][self.empty_col] = self.puzzle[self.empty_row-1][self.empty_col], self.puzzle[self.empty_row][self.empty_col]
                self.empty_row -= 1
            elif move == 'r':
                self.puzzle[self.empty_row][self.empty_col], self.puzzle[self.empty_row][self.empty_col+1] = self.puzzle[self.empty_row][self.empty_col+1], self.puzzle[self.empty_row][self.empty_col]
                self.empty_col += 1
            elif move == 'l':
                self.puzzle[self.empty_row][self.empty_col], self.puzzle[self.empty_row][self.empty_col-1] = self.puzzle[self.empty_row][self.empty_col-1], self.puzzle[self.empty_row][self.empty_col]
                self.empty_col -= 1
            self.moves.append(move)
            # self.print_puzzle()

    def focus_tile_top(self, tile_real_row_col: list[int]) -> None:
        """Move the empty tile such that it is immediately above the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it is below a solved tile.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = tile_real_row_col
        if tile_real_row == self.size - 1:
            while self.empty_row < tile_real_row - 1:
                self.move('d')
            while self.empty_row > tile_real_row - 1:
                self.move('u')
            while self.empty_col < tile_real_col:
                self.move('r')
            while self.empty_col > tile_real_col:
                self.move('l')
        else:
            self.focus_tile_bottom(tile_real_row_col)
            self.move('u')
            tile_real_row_col[0] += 1

    def focus_tile_bottom(self, tile_real_row_col: list[int]) -> None:
        """Move the empty tile such that it is immediately below the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it is already at the bottom.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = tile_real_row_col
        if self.empty_col == tile_real_col and self.empty_row < tile_real_row:
            one_off = 0
            tile_real_row_col[0] -= 1
        else:
            one_off = 1
        while self.empty_row < tile_real_row + one_off:
            self.move('d')
        while self.empty_row > tile_real_row + one_off:
            self.move('u')
        while self.empty_col < tile_real_col:
            self.move('r')
        while self.empty_col > tile_real_col:
            self.move('l')

    def focus_tile_left(self, tile_real_row_col: list[int]) -> None:
        """Move the empty tile such that it is immediately left to the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it is all the way to the left.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = tile_real_row_col

        if self.empty_col == tile_real_col and self.empty_row + 1 == tile_real_row:
            if self.empty_col == self.size - 1:
                self.move('ld')
            else:
                self.move('rd')
        elif self.empty_row < self.size - 1:
            self.move('d')

        if tile_real_col == self.size - 1:
            while self.empty_col < tile_real_col - 1:
                self.move('r')
            while self.empty_col > tile_real_col - 1:
                self.move('l')
            while self.empty_row < tile_real_row:
                self.move('d')
            while self.empty_row > tile_real_row:
                self.move('u')
        else:
            self.focus_tile_right(tile_real_row_col)
            self.move('l')
            tile_real_row_col[1] += 1

    def focus_tile_right(self, tile_real_row_col: list[int]) -> None:
        """Move the empty tile such that it is immediately right to the target :tile,
        without affecting already solved tiles.
        This might move the target :tile if it all the way to the right.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        tile_real_row, tile_real_col = tile_real_row_col

        if self.empty_col == tile_real_col and self.empty_row + 1 == tile_real_row:
            if self.empty_col == self.size - 1:
                self.move('ld')
            else:
                self.move('rd')
        elif self.empty_row < self.size - 1:
            self.move('d')

        if self.empty_row == tile_real_row and self.empty_col < tile_real_col:
            one_off = 0
            tile_real_row_col[1] -= 1
        else:
            one_off = 1
        while self.empty_col < tile_real_col + one_off:
            self.move('r')
        while self.empty_col > tile_real_col + one_off:
            self.move('l')
        while self.empty_row < tile_real_row:
            self.move('d')
        while self.empty_row > tile_real_row:
            self.move('u')

    def move_horizontally_using_bottom(self, tile_real_row_col: list[int], tile_target_row_col: list[int]) -> bool:
        """Return True if the immediate top position of the tile to be moved
        is ideal/necessary for horizontal movement, False otherwise.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted.
        """
        if tile_real_row_col[0] == self.size - 1:
            return False
        elif tile_real_row_col[0] == tile_target_row_col[0]:
            return True
        elif tile_real_row_col[0] == tile_target_row_col[0] + 1:
            if tile_real_row_col[1] < tile_target_row_col[1]:
                return True
            return self.empty_row >= tile_real_row_col[0]
        return self.empty_row >= tile_real_row_col[0]

    def move_vertically_using_right(self, tile_real_row_col: list[int], tile_target_row_col: list[int]) -> bool:
        """Return True if the immediate right position of the tile to be moved
        is ideal/necessary for vertical movement, False otherwise.
        Requires that the puzzle is solved top-to-bottom, left-to-right and
        requires at least 2 unsolved rows below the row where the tile is
        supposed to be inserted and
        (requires tile to be aligned horizontally to work optimally).
        """
        if tile_real_row_col[1] == self.size - 1:
            return False
        return True

    def align_tile_horizontally(self, tile_real_row_col: list[int], tile_target_row_col: list[int], repositioning_moves: str) -> None:
        """Move tile left or right until it reaches :tile_col.
        """
        first = True
        while tile_real_row_col[1] < tile_target_row_col[1]:
            if first:
                self.focus_tile_right(tile_real_row_col)
                first = False
            else:
                self.move(repositioning_moves)
            self.move('l')
            tile_real_row_col[1] = tile_real_row_col[1] = tile_real_row_col[1] + 1
        while tile_real_row_col[1] > tile_target_row_col[1]:
            if first:
                self.focus_tile_left(tile_real_row_col)
                first = False
            else:
                self.move(repositioning_moves)
            self.move('r')
            tile_real_row_col[1] = tile_real_row_col[1] = tile_real_row_col[1] - 1

    def align_tile_vertically(self, tile_real_row_col: list[int], tile_target_row_col: list[int], repositioning_moves: str) -> None:
        """Move tile top or down until it reaches :tile_row.
        """
        first = True
        while tile_real_row_col[0] < tile_target_row_col[0]:
            if first:
                self.focus_tile_bottom(tile_real_row_col)
                first = False
            else:
                self.move(repositioning_moves)
            self.move('u')
            tile_real_row_col[0] = tile_real_row_col[0] = tile_real_row_col[0] + 1
        while tile_real_row_col[0] > tile_target_row_col[0]:
            if first:
                self.focus_tile_top(tile_real_row_col)
                first = False
            else:
                self.move(repositioning_moves)
            self.move('d')
            tile_real_row_col[0] = tile_real_row_col[0] = tile_real_row_col[0] - 1

    def get_horizontal_repositioning_moves(self, tile_real_row_col: list[int], tile_target_row_col: list[int]) -> str:
        """Return the needed repositioning moves after a tile has been moved
        horizontally to make the moving of the tile repeatable.
        """
        if self.move_horizontally_using_bottom(tile_real_row_col, tile_target_row_col):
            if tile_real_row_col[1] < tile_target_row_col[1]:
                repositioning_moves = 'drru'
            else:
                repositioning_moves = 'dllu'
        else:
            if tile_real_row_col[1] < tile_target_row_col[1]:
                repositioning_moves = 'urrd'
            else:
                repositioning_moves = 'ulld'
        return repositioning_moves

    def get_vertical_repositioning_moves(self, tile_real_row_col: list[int], tile_target_row_col: list[int]) -> str:
        """Return the needed repositioning moves after a tile has been moved
        vertically to make the moving of the tile repeatable.
        """
        if self.move_vertically_using_right(tile_real_row_col, tile_target_row_col):
            if tile_real_row_col[0] < tile_target_row_col[0]:
                repositioning_moves = 'rddl'
            else:
                repositioning_moves = 'ruul'
        else:
            if tile_real_row_col[0] < tile_target_row_col[0]:
                repositioning_moves = 'lddr'
            else:
                repositioning_moves = 'luur'
        return repositioning_moves

    def solve_row_n_minus_2_tiles(self, row: int) -> None:
        """Solve first n-2 tiles of a particular :row.
        Requires that all previous rows are completely solved.
        """
        first_tile = row * self.size + 1
        last_tile = first_tile + self.size - 3
        for tile in range(first_tile, last_tile + 1):
            tile_target_row_col = list(divmod(tile - 1 if tile != 0 else self.size ** 2 - 1, self.size))
            tile_real_row_col = list(self._get_tile_pos(tile))

            repositioning_moves_horizontal = self.get_horizontal_repositioning_moves(tile_real_row_col, tile_target_row_col)
            self.align_tile_horizontally(tile_real_row_col, tile_target_row_col, repositioning_moves_horizontal)
            repositioning_moves_vertical = self.get_vertical_repositioning_moves(tile_real_row_col, tile_target_row_col)
            self.align_tile_vertically(tile_real_row_col, tile_target_row_col, repositioning_moves_vertical)

    def solve_row_last_2_tiles(self, row: int) -> None:
        """Solve last 2 tiles of a particular :row.
        Requires that all previous tiles in that row are solved.
        """
        P = (row + 1) * self.size - 1 # == Penultimate Tile Index
        PT = list(divmod(P - 1 if P != 0 else self.size ** 2 - 1, self.size)) # Penultimate Tile Target Row & Col
        # mutable list needed to pass it down to funcs as ref without creating bloated object or creating non-generic methods
        PR = list(self._get_tile_pos(P)) # Penultimate Tile Real Row & Col

        L = P + 1 # == Last Tile Index
        LT = list(divmod(L - 1 if L != 0 else self.size ** 2 - 1, self.size)) # Last Tile Target Row & Col
        # see comment above
        LR = list(self._get_tile_pos(L)) # Last Tile Real Row & Col

        if PR == LT and \
           LR == PT: # last 2 tiles are swapped?
            # transform to a case handled later

            self.focus_tile_bottom(LR) # safe, won't move P or L
            self.move('ur') # This depends on the previous action not moving P or L
            LR[0] += 1 # P and L have have moved, we must reflect that
            PR[1] -= 1
        elif [self.empty_row, self.empty_col] == PT and \
             PR == LT: # empty tile in target of P and P in target of L?
            self.move('r')
            PR[1] -= 1

        if PR == PT: # P is in correct position?
            if LR == LT: # L is also in correct position? Well, then we're done
                return

            elif LR[0] == LT[0] + 1 and \
                 LR[1] == LT[1]: # L is in correct column, but one below its target row?
                    self.focus_tile_bottom(LR) # This might move L into its target row
                    if LR == LT: # if that is the case, we're done
                        return

                    self.move('uuldrdluurd') # solve the row

            elif LR[0] == LT[0] + 1 and \
                 LR[1] == LT[1] - 1: # L is bottom-left (diagonally) of its target position?
                    if self.empty_row == LT[0] + 1 and \
                       self.empty_col < LR[1]: # empty is in the same row and left to L?
                        self.move('r' * (1 + LR[1] - self.empty_col)) # move empty all the way to the right (moving L one tile to its left)
                        self.move('uldldrrulurd') # solve the row

                    else: # empty is not (in the same row and left to L)
                        if self.empty_row <= LT[0] + 1 and \
                           self.empty_col > LR[1]: # empty is in the same row or above the row of L and to the right of L?
                            self.move('d' * (LT[0] + 1 - self.empty_row + 1)) # move empty down until its row is right below L

                        self.move('u' * (self.empty_row - LT[0] - 2)) # if we're too low, move empty up until we're right below L
                        if self.empty_col > LR[1]: # empty is right of L
                            self.move('l' * (self.empty_col - LR[1])) # move empty left

                        elif self.empty_col < LR[1]: # empty is left of L
                            self.move('r' * (LR[1] - self.empty_col)) # move empty right

                        self.move('urulddrulurd') # solve the row

            else: # L is anywhere else?
                if self.empty_col < self.size - 1 and \
                   self.empty_col == LR[1] and \
                   self.empty_row == LR[0] - 1: # empty right above L and not in last column?
                    self.move('r') # to avoid causing that edge that we haven't proven that it won't happen again (see TODO below)
                self.focus_tile_right(PR) # go to right of P, this might move L
                self.move('l') # move P to the right
                PR[1] += 1 # reflect that
                # TODO: prove that L will never be at (PT[0]+1, PT[1])
                LR[0], LR[1] = self._get_tile_pos(L) # get L in case it changed, also splitting it to update the references
                repositioning_moves_horizontal = self.get_horizontal_repositioning_moves(LR, LT) # determine moving strategory
                self.align_tile_horizontally(LR, LT, repositioning_moves_horizontal) # move L to its column
                LT[0] += 1 # increase target row by one, because L is supposed to be right below the new P
                self.align_tile_vertically(LR, LT, 'luur') # move L up, right below P
                self.focus_tile_left(PR) # go to left of P
                self.move('rd') # solve the row
        elif PR == LT: # P is in L's target position?
            # L won't be in P's target position, we checked that case already
            repositioning_moves_horizontal = self.get_horizontal_repositioning_moves(LR, LT)
            self.align_tile_horizontally(LR, LT, repositioning_moves_horizontal) # won't move P
            LT[0] += 1 # we want L to be right below P
            self.align_tile_vertically(LR, LT, 'luur') # won't move P
            self.focus_tile_bottom(LR) # in case the vertical alignment didn't happen, we might be at a (not really) random location, so ensure focus below R (will not move P)
            self.move('luurd') # solve the row
        elif PR[1] == self.size - 1 and \
             LR == LT: # L is solved and P is somewhere in the last column?
            if PR[0] < self.size - 1: # P is NOT in the last row?
                self.focus_tile_bottom(PR) # focus below P (which only works if it's not in the last row)
                PR[0] += 1 # we are below P. The next step is going to focus L, which is above. Thereforce, P will move down (increasing the row)

            self.focus_tile_bottom(LR)
            self.move('uldr') # put L bottom-left (diagonally) of its target position
            self.align_tile_vertically(PR, PT, 'luur') # move P to LT
            # now L is either at 1. (LT[0]+2, LT[1]-1) or 2. (LT[0]+2, LT[1])
            self.move('d')
            if self.puzzle[LT[0] + 2][LT[1]-1] == L: # if L is at (LT[0]+2, LT[1]-1)
                self.move('lurd') # synchronize, now L will be at the same position that it would be if it was at 2. to begin with
            self.move('luurd') # solve the row
        else: # P is anywhere else, or the last column if L is not solved
            PT[1] += 1 # goal is to move P to LT
            repositioning_moves_horizontal = self.get_horizontal_repositioning_moves(PR, PT)
            self.align_tile_horizontally(PR, PT, repositioning_moves_horizontal) # TODO: prove that this will never cause one of the other cases
            if LR != LT:
                self.align_tile_vertically(PR, PT, 'luur') # this is safe and won't put L into a weird place
            # no we are in a case that is already handled above (P being in LT)
            self.solve_row_last_2_tiles(row)

    def solve_n_minus_2_rows(self) -> None:
        """Solve first n-2 rows of the puzzle.
        No additional requirements.
        """
        for row in range(self.size - 2):
            self.solve_row_n_minus_2_tiles(row)
            self.solve_row_last_2_tiles(row)

    def last_2_rows_prepare_T(self, TR: list[int], TT: list[int]) -> None:
        """Move the top tile into the bottom tile's target position as a preliminary
        step.
        """
        if TR[0] == TT[0] + 1 and \
           TR[1] == TT[1]: # target tile is already in BT?
            if self.empty_row != TT[0]: # empty is in bottom row?
                self.move('u')
            if self.empty_col < TR[1]: # empty is left of T?
                assert False # this branch should not be possible
                # self.move('r' * (TR[1] - self.empty_col))
            else: # empty is right of T? (this should always happen)
                self.move('l' * (self.empty_col - TR[1]))
            return # T is now at BT and empty is right above

        if TR[0] == TT[0]: # T is in its target row? (it should be below)
            if self.empty_row == TT[0]: # empty is also in target tile's row?
                self.move('d')
            if self.empty_col < TR[1]: # empty is left of T?
                self.move('r' * (TR[1] - self.empty_col))
            else: # empty is right of T?
                self.move('l' * (self.empty_col - TR[1]))
            self.move('u')
            TR[0] += 1

        else: # T is in bottom row?
            if self.empty_row != TT[0]: # empty is also in bottom row?
                self.move('u')
            if self.empty_col < TR[1]: # empty is left of T?
                self.move('r' * (TR[1] - self.empty_col))
            else: # empty is right of T?
                self.move('l' * (self.empty_col - TR[1]))

        # T as at bottom row, empty is right above, and T is not at BT (it must be moved)
        self.move('ldrul' * (TR[1] - TT[1]))
        # T is now at BT and empty is right above

    def last_2_rows_prepare_B(self, BR: list[int], BT: list[int]) -> None:
        """Move the bottom tile to the right of the top tile (where the bottom
        tile will be moved to later).
        Requires the top tile to be in the target position of the bottom tile and
        requires the empty tile to be right above the top tile.
        """
        if self.empty_row == BR[0] and \
           self.empty_col == BR[1] - 1: # edge case where B is right of empty
               self.move('drrulldruldrurdlurd') # prepare
               return
        if BR[0] == BT[0] - 1: # B is in top row? (we need to move it down)
            self.move('r' * (BR[1] - self.empty_col - 1))
            self.move('dru')
        else: # B is in bottom row?
            self.move('r' * (BR[1] - self.empty_col))
        self.move('ldrul' * (BR[1] - BT[1] - 1))
        self.move('rd')

    def solve_last_2_rows_col(self, col: int) -> None:
        """Solve a particular :col from the last 2 rows.
        Requires that all previous columns in the last 2 rows are solved.
        """
        T = self.size * (self.size - 2) + 1 + col # Top Tile Index
        TT = list(divmod(T - 1 if T != 0 else self.size ** 2 - 1, self.size)) # Top Tile Target Row & Col
        # mutable list needed to pass it down to funcs as ref without creating bloated object or creating non-generic methods
        TR = list(self._get_tile_pos(T)) # Top Tile Real Row & Col

        self.last_2_rows_prepare_T(TR, TT)

        B = T + self.size # Bottom Tile Index
        BT = list(divmod(B - 1 if B != 0 else self.size ** 2 - 1, self.size)) # Bottom Tile Target Row & Col
        # see comment above
        BR = list(self._get_tile_pos(B)) # Bottom Tile Real Row & Col

        self.last_2_rows_prepare_B(BR, BT)

        self.move('ulldr') # solve column

    def solve_last_2_rows_n_minus_2_cols(self) -> None:
        """Solve the first n-2 columns of the last 2 rows.
        Requires that all previous rows are solved.
        """
        for col in range(self.size - 2):
            self.solve_last_2_rows_col(col)

    def solve_last_4_tiles(self) -> None:
        """Solve bottom right 4 tiles. If not self.is_solvable, then this step
        will fail.
        Requires that all tiles of the puzzle are solved, except these last 4.
        """
        UR = list(self._get_tile_pos(self.size ** 2 - 1)) # ultimate tile, the very last tile (biggest value)
        if self.empty_row == UR[0] and \
           self.empty_col == UR[1] - 1: # ultimate tile is in target position of empty
            self.move('r')
        elif self.empty_row == UR[0] + 1 and \
             self.empty_col == UR[1]: # ultimate tile is above empty
            self.move('urd')
        elif self.empty_row == UR[0] + 1 and \
             self.empty_col == UR[1] - 1: # ultimate tile is top-right (diagonally) of the empty tile
            self.move('ruldr')
        else: # already solved!
            return

    def solve_last_2_rows(self) -> None:
        """Solve last two rows of the puzzle.
        Requires that all previous rows are solved.
        """
        self.solve_last_2_rows_n_minus_2_cols()
        self.solve_last_4_tiles()

    def solve(self) -> None:
        """Turn the puzzle back to its standard configuration and save the moves
        in self.moves
        Takes probably at least O(n**3) multiplied by some big constant, or more.
        Requires that the puzzle is solvable.
        """
        if not puzzle._is_solvable():
            puzzle.error('Puzzle not solvable', 0)
            return
        self.solve_n_minus_2_rows()
        self.solve_last_2_rows()

if __name__ == '__main__':
    puzzle = Puzzle(open(0))
    elapsed_seconds = timeit.timeit('puzzle.solve()', globals=globals(), number=1)

    print(f'Time: {elapsed_seconds:.6f}s, Moves: {len(puzzle.moves)}', file=sys.stderr, flush=True)
    print(''.join(puzzle.moves))

    if len(puzzle.moves) == 0 and puzzle.is_solvable:
        raise SystemExit(1)
    elif not puzzle.is_solvable:
        raise SystemExit(2)
    raise SystemExit(0)
