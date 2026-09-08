def _add_book_with_genre(self, collector, book_name, genre):
    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)

def _add_books_for_testing(self, collector):
    books = {"Метро 2033": "Фантастика", "Дюна": "Фантастика", "Большой Куш": "Комедия"}
    for name, genre in books.items():
        self.add_book_with_genre(collector, name, genre)
