"""
Contains layouts for different grid warehouses
"""

from models import GridWarehouse, NavigableTileCell, ShelvingColumnCell, Direction, Shelve, Book
from books import BooksRepository
import utils
import copy
import os
import json


def get_simple_warehouse():
    dimensions = (4, 4)

    grid = utils.init_grid(dimensions)

    # Fill out first column, bottom to top
    grid[0][0] = NavigableTileCell()
    grid[0][1] = NavigableTileCell()
    grid[0][2] = NavigableTileCell()
    grid[0][3] = NavigableTileCell()

    # Fill out second column, bottom to top
    grid[1][0] = NavigableTileCell()
    grid[1][1] = ShelvingColumnCell(Direction.SOUTH)
    grid[1][2] = ShelvingColumnCell(Direction.NORTH)
    grid[1][3] = NavigableTileCell()

    # Fill out third column, bottom to top
    grid[2][0] = NavigableTileCell()
    grid[2][1] = ShelvingColumnCell(Direction.SOUTH)
    grid[2][2] = ShelvingColumnCell(Direction.NORTH)
    grid[2][3] = NavigableTileCell()

    # Fill out fourth column, bottom to top
    grid[3][0] = NavigableTileCell()
    grid[3][1] = NavigableTileCell()
    grid[3][2] = NavigableTileCell()
    grid[3][3] = NavigableTileCell()

    warehouse = GridWarehouse(dimensions, grid)

    return warehouse


def get_larger_warehouse():
    dimensions = (8, 4)

    grid = utils.init_grid(dimensions)

    for row_num in range(4):
        grid[0][row_num] = NavigableTileCell()

    for col_num in range(1, 7):
        grid[col_num][0] = NavigableTileCell()
        grid[col_num][1] = ShelvingColumnCell(Direction.NORTH)
        grid[col_num][2] = ShelvingColumnCell(Direction.SOUTH)
        grid[col_num][3] = NavigableTileCell()

    for row_num in range(4):
        grid[7][row_num] = NavigableTileCell()

    warehouse = GridWarehouse(dimensions, grid)

    return warehouse


def get_georgia_tech_library_warehouse():
    larger_warehouse = get_larger_warehouse()
    larger_warehouse_grid = larger_warehouse.grid

    dimensions = (8, 16)
    grid = utils.init_grid(dimensions)

    for col_num in range(8):
        for row_num in range(16):
            grid[col_num][row_num] = copy.copy(larger_warehouse_grid[col_num][row_num % 4])

    return GridWarehouse(dimensions, grid)


def w():
    dimensions = (8, 4)

    grid = utils.init_grid(dimensions)

    books_repository = BooksRepository(os.path.join('data', 'books.json'))

    for row_num in range(4):
        grid[0][row_num] = NavigableTileCell()

    for col_num in range(1, 7):
        grid[col_num][0] = NavigableTileCell()
        grid[col_num][1] = get_shelving_column(books_repository, Direction.NORTH, 'A', str(110 - col_num * 2))
        grid[col_num][2] = get_shelving_column(books_repository, Direction.SOUTH, 'B', str(111 - col_num * 2))
        grid[col_num][3] = NavigableTileCell()

    for row_num in range(4):
        grid[7][row_num] = NavigableTileCell()

    warehouse = GridWarehouse(dimensions, grid)

    return warehouse


def get_shelving_column(books_repository, direction, aisle_label, column_label):
    books = books_repository.get_books(aisle_label, column_label)

    shelves = []
    for book in books:
        if book is None:  # this shelve is empty
            shelves.append(None)
        else:
            shelves.append(Shelve(
                shelve_label=book['location']['row'],
                item=Book(
                    title=book['book']['title'],
                    author=book['book']['author'])
            ))

    return ShelvingColumnCell(
        aisle_label=aisle_label,
        column_label=column_label,
        direction=direction,
        shelves=shelves,
    )
