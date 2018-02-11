import json


class BooksRepository(object):
    ROW_LABELS = list('ABCDEF')

    def __init__(self, books_file_path):
        with open(books_file_path, mode='r') as books_file:
            self.books = json.load(books_file)

    def get_books(self, in_aisle, on_shelving_column):
        books = []
        # Return the books in position from bottom to top (F to A)
        for row_label in self.ROW_LABELS[::-1]:
            books.append(self.get_book(in_aisle, on_shelving_column, row_label))
        return books

    def get_book(self, in_aisle, on_shelving_column, on_row):
        for book in self.books:
            location = book['location']

            if location['aisle'] == in_aisle \
                and location['column'] == on_shelving_column \
                and location['row'] == on_row:
                return book

        return None
