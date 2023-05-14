from collections import defaultdict
from itertools import repeat
from typing import Iterable, Sequence
from util import try_int
import numpy as np
import numpy.typing as npt
import re


fmt_dict = {"strip": False, "sep": "\n\n"}

IntegerPair = tuple[int, int]
IntegerArray = npt.NDArray[np.int_]
BoardState = tuple[int, int, int, int]
TileAdjacencyMap = dict[IntegerPair, dict[IntegerPair, tuple[int, int, int]]]
BoardStateMap = dict[BoardState, BoardState]


DIRECTION_TO_INDEX: dict[IntegerPair, int] = {
    (0, 1): 0,
    (1, 0): 1,
    (0, -1): 2,
    (-1, 0): 3,
}

INDEX_TO_DIRECTION: dict[int, IntegerPair] = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


class CyclicBoard:
    def __init__(
        self, board: IntegerArray, tile_size: int, adjacencies: TileAdjacencyMap
    ):
        self.__m, self.__n = board.shape
        self.__s = tile_size
        self.__edges = self.__get_edges(adjacencies)

    def __get_ranges(
        self, i: int, j: int, di: int, dj: int, reverse: bool = False
    ) -> tuple[Iterable[int], Iterable[int]]:
        match (di, dj):
            case (0, 1):
                range_j = repeat(self.__s * (j + 1) - 1, self.__s)
                range_i = range(self.__s * i, self.__s * (i + 1))
                if reverse:
                    range_i = reversed(range_i)
            case (1, 0):
                range_i = repeat(self.__s * (i + 1) - 1, self.__s)
                range_j = range(self.__s * j, self.__s * (j + 1))
                if not reverse:
                    range_j = reversed(range_j)
            case (0, -1):
                range_j = repeat(self.__s * j, self.__s)
                range_i = range(self.__s * i, self.__s * (i + 1))
                if not reverse:
                    range_i = reversed(range_i)
            case (-1, 0):
                range_i = repeat(self.__s * i, self.__s)
                range_j = range(self.__s * j, self.__s * (j + 1))
                if reverse:
                    range_j = reversed(range_j)
        return range_i, range_j

    def __get_edges(self, adjacencies: TileAdjacencyMap) -> BoardStateMap:
        edges = {}
        for (i1, j1), d in adjacencies.items():
            for (di, dj), (i2, j2, r) in d.items():
                r_i1, r_j1 = self.__get_ranges(i1, j1, di, dj)
                r_i2, r_j2 = self.__get_ranges(
                    i2, j2, *CyclicBoard.rotate(di, dj, 2 + r), reverse=True
                )
                for x1, y1, x2, y2 in zip(r_i1, r_j1, r_i2, r_j2):
                    edges[(x1, y1, di, dj)] = (
                        x2,
                        y2,
                        *CyclicBoard.rotate(di, dj, r),
                    )
        return edges

    @staticmethod
    def rotate(di: int, dj: int, r: int) -> IntegerPair:
        return INDEX_TO_DIRECTION[(DIRECTION_TO_INDEX[(di, dj)] + r) % 4]

    def next(self, i: int, j: int, di: int, dj: int) -> BoardState:
        return self.__edges.get(
            (i, j, di, dj),
            (
                i + di,
                j + dj,
                di,
                dj,
            ),
        )


class MonkeyMap:
    _TILE_KEY = {" ": 0, ".": 1, "#": 2}
    _TURN_KEY = {"L": -1, "R": 1}

    def __init__(self, board, path: Iterable[int | str]):
        self.__board = board
        self.__path = path
        self.__s = MonkeyMap.__get_side_length(board)
        self.__initial_state = *MonkeyMap.__get_starting_position(board), 0, 1
        self.__m, self.__n = [dim // self.__s for dim in board.shape]
        self.__tiles = {
            (i, j)
            for i in range(self.__m)
            for j in range(self.__n)
            if board[self.__s * i, self.__s * j]
        }

    @classmethod
    def from_data(cls, data: Sequence[str]):
        return cls(MonkeyMap.__parse_board(data[0]), MonkeyMap.__parse_path(data[1]))

    @staticmethod
    def __parse_board(b: str) -> IntegerArray:
        lines = b.split("\n")
        board = np.zeros((len(lines), max(map(len, lines))), dtype=int)
        for i, line in enumerate(lines):
            for j, tile in enumerate(line):
                board[i, j] = MonkeyMap._TILE_KEY[tile]
        return board

    @staticmethod
    def __parse_path(p: str) -> Iterable[int | str]:
        return tuple(map(try_int, re.findall("\d+|[RL]", p)))

    @staticmethod
    def __get_side_length(board: IntegerArray) -> int:
        return min(
            map(
                MonkeyMap.__get_min_span,
                (board[0], board[-1], board[:, 0], board[:, -1]),
            )
        )

    @staticmethod
    def __get_min_span(seq: Iterable) -> int:
        min_span = None
        i_start = None
        for i, elem in enumerate(seq):
            if elem:
                if i_start is None:
                    i_start = i
            elif i_start is not None:
                min_span = (
                    i - i_start if min_span is None else min(min_span, i - i_start)
                )
        if i_start is not None:
            min_span = (
                i - i_start + 1 if min_span is None else min(min_span, i - i_start + 1)
            )
        return min_span or 0

    @staticmethod
    def __get_starting_position(board: IntegerArray) -> IntegerPair:
        for i, row in enumerate(board):
            for j, elem in enumerate(row):
                if elem == 1:
                    return i, j
        raise ValueError("board has no open tiles")

    def __get_adjacencies_2d(self) -> TileAdjacencyMap:
        adjs = defaultdict(dict)
        for i, j in self.__tiles:
            for di, dj in DIRECTION_TO_INDEX:
                ii, jj = i + di, j + dj
                if (ii, jj) in self.__tiles:
                    continue
                for _ in range(self.__m if di else self.__n):
                    ii, jj = ii % self.__m, jj % self.__n
                    if (ii, jj) in self.__tiles:
                        adjs[i, j][di, dj] = (ii, jj, 0)
                        break
                    ii, jj = ii + di, jj + dj
        return adjs

    def __get_adjacencies_3d(self) -> TileAdjacencyMap:
        adjs = defaultdict(dict)
        seen_tiles = set()
        q = [
            (
                next(iter(self.__tiles)),
                np.array([0, 0, 1]),
                np.array([1, 0, 0]),
                np.array([0, 1, 0]),
            )
        ]
        info_by_tile = {}
        info_by_normal = {}
        while q:
            t, n, u, v = q.pop()
            seen_tiles.add(t)
            info_by_tile[t] = n, u, v
            info_by_normal[tuple(n)] = t, u, v
            i, j = t
            for di, dj in DIRECTION_TO_INDEX:
                t2 = (i + di, j + dj)
                if t2 not in self.__tiles or t2 in seen_tiles:
                    continue
                vectors = (
                    (di * np.cross(v, n), di * np.cross(v, u), v)
                    if di
                    else (dj * np.cross(n, u), u, dj * np.cross(v, u))
                )
                q.append((t2, *vectors))
        for (i1, j1), (n1, u1, v1) in info_by_tile.items():
            for di, dj in DIRECTION_TO_INDEX:
                n2 = di * u1 + dj * v1
                (i2, j2), u2, v2 = info_by_normal[tuple(n2)]
                if (i2, j2) == (i1 + di, j1 + dj):
                    continue
                R = get_rotation_matrix(n1, n2)
                u1_t = R @ u1
                r = [0, 0, -2][np.dot(u1_t, u2)] - np.dot(u1_t, v2)
                adjs[(i1, j1)][di, dj] = i2, j2, r
        return adjs

    def __step(self, cyclic_board: CyclicBoard) -> bool:
        i, j, di, dj = cyclic_board.next(self.__i, self.__j, self.__di, self.__dj)
        if self.__board[i, j] == 1:
            self.__i, self.__j, self.__di, self.__dj = i, j, di, dj
            return True
        return False

    def __move(self, cyclic_board: CyclicBoard, n: int) -> None:
        for _ in range(n):
            if not self.__step(cyclic_board):
                break

    def __rotate(self, direction: str) -> None:
        self.__di, self.__dj = CyclicBoard.rotate(
            self.__di, self.__dj, MonkeyMap._TURN_KEY[direction]
        )

    def __score(self) -> int:
        return (
            1000 * (self.__i + 1)
            + 4 * (self.__j + 1)
            + DIRECTION_TO_INDEX[(self.__di, self.__dj)]
        )

    def __simulate(self, adjacencies: TileAdjacencyMap) -> int:
        self.__i, self.__j, self.__di, self.__dj = self.__initial_state
        cyclic_board = CyclicBoard(self.__board, self.__s, adjacencies)
        for instr in self.__path:
            if isinstance(instr, int):
                self.__move(cyclic_board, instr)
            else:
                self.__rotate(instr)
        return self.__score()

    def solve(self) -> IntegerPair:
        return self.__simulate(self.__get_adjacencies_2d()), self.__simulate(
            self.__get_adjacencies_3d()
        )


def get_rotation_matrix(n1: IntegerArray, n2: IntegerArray) -> IntegerArray:
    u = np.cross(n1, n2)
    W = np.array([[0, -u[2], u[1]], [u[2], 0, -u[0]], [-u[1], u[0], 0]])
    return np.eye(3, dtype=int) + W + W @ W


def solve(data: Sequence[str]):
    return MonkeyMap.from_data(data).solve()
