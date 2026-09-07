import pytest
from main import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        return BooksCollector()
    def _add_book_with_genre(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
    def _add_books_for_testing(self, collector):
        books = {"Метро 2033": "Фантастика", "Дюна": "Фантастика", "Большой Куш": "Комедия"}
        for name, genre in books.items():
            self.add_book_with_genre(collector, name, genre)

    #Тесты для add_new_book
    @pytest.mark.parametrize("book_name", ["Война и Мир", "Мастер и Маргарита", "Гарри Поттер и филосовский камень", "А" * 40])
    def test_add_new_book_success(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre
        assert collector.books_genre[book_name] == ""

    @pytest.mark.parametrize("book_name", ["", "A" * 41])
    def test_add_new_book_invalid_lenght(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    def test_add_new_book_duplicate(self, collector):
        book_name = "Библия"
        collector.add_new_book(book_name)
        collector.add_new_book(book_name)
        assert collector.books_genre.get(book_name) == ""
        assert sum(1 for key in collector.books_genre if key == book_name) == 1

    #Тесты для set_book_genre
    @pytest.mark.parametrize("book_name, genre", [
        ("Метро 2033", "Фантастика"), ("Оно", "Ужасы"),
        ("Убийство в Восточном экспрессе", "Детективы"), ("Шрек", "Мультфильм"),
        ("Джентельмены", "Комедии")
        ])
    def test_book_genre_success(self, collector, book_name, genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    def test_set_book_genre_book_not_exists(self, collector):
        collector.set_book_genre("Наскальная нахальность", "Фантастика")
        assert "Наскальная нахальность" not in collector.books_genre

    @pytest.mark.parametrize("genre", ["Неизвестный жанр", "Драма", "Триллер", "Роман"])
    def test_set_book_genre_invalid_genre(self, collector, genre):
        book_name = "Тест книга"
        collector.add_new_book_genre(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == ""

    #Тесты для get_book_genre
    def test_get_book_genre_existing_book(self, collector):
        book_name = "Новый Вавилон"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.get_book_genre(book_name) == "Фантастика"

    def test_get_book_not_existing_book(self, collector):
        assert collector.get_book_genre("Наскальная нахальность") is None

    def test_get_book_genre_no_genre_set(self, collector):
        book_name = "Книга без жанра"
        collector.add_new_book(book_name)
        assert collector.get_book_genre(book_name) == ""

    #Тесты для get_books_with_specific_genre
    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Метро 2033", "Дюна"]),
        ("Ужасы", ["Оно"]),
        ("Комедии", []),
        ("Неизвестный жанр", [])
    ])
    def test_get_books_wuth_specific_genre(self, collector, genre, expected_books):
        self.add_books_for_testing(collector)
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected_books

    def test_get_books_with_specific_genre_empty(self, collector):
        assert collector.get_books_with_specific_genre("Фантастика") ==[]

    #Тесты для get_books_genre
    def test_get_books_genre_returns_dict(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        result = collector.get_books_genre()
        assert isinstance(result, dict)
        assert "Книга 1" in result
        assert "Книга 2" in result

    def test_get_books_genre_empty(self, collector):
        assert collector.get_books_genre() == {}

    #Тесты для get_books_for_children
    def test_get_books_for_children_mixed_genre(self, collector):
        collector.add_new_book("Винни-Пух")
        collector.set_book_genre("Винни-Пух", "Мультфильм")

        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")

        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")

        collector.add_new_book("Убийство в Восточном экспрессе")
        collector.set_book_genre("Убийство в Восточном экспрессе", "Детектив")

        children_books = collector.get_books_for_children()
        assert "Винни-Пух" in children_books
        assert "Гарри Поттер" in children_books
        assert "Оно" in children_books
        assert "Убийство в Восточном экспрессе" in children_books

    def test_get_books_for_children_empty(self, collector):
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_books_for_children() == []

    def test_get_books_for_children_no_books(self, collector):
        assert collector.get_books_for_children() == []

    #Тесты для add_book_in_favorites
    @pytest.mark.parametrize("book_name", ["Мастер и Маргарита", "Преступление и наказание", "Собачье Сердце"])
    def test_add_book_in_favorites_success(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites

    def test_add_book_in_favorites_not_in_books_genre(self, collector):
        collector.add_book_in_favorites("Наскальная нахальность")
        assert "Наскальная нахальность" not in collector.favorites
        
    def test_add_book_in_favorites_duplicate(self, collector):
        book_name = "Дубровский"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        assert collector.favorites.count(book_name) == 1

    def test_add_book_in_favorites_without_genre(self, collector):
        book_name = "Книга без жанра"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites

    #Тесты для delete_book_from_favorites
    @pytest.mark.parametrize("Book_name", ["Масетр и Маргарита", "Преступление и наказание", "Собачье сердце"])
    def test_delete_book_from_favorites_success(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites

        collector.delete_book_form_favorites(book_name)
        assert book_name not in collector.favorites
        
    def test_delete_book_from_favorites_not_in_favorites(self, collector):
        collector.add_new_book("Книга 1")
        collector.delete_book_from_favorites("Книга 1")
        assert collector.favorites == []

    def test_delete_book_from_favorites_not_in_books_genre(self,collector):
        collector.delete_book_from_favorites("Наскальная нахальность")
        assert collector.favorites == []

    #Тесты для get_list_of_favorites_books
    def test_get_list_of_favorites_books_with_books(self, collector):
        books = ["Книга 1", "Книга 2", "Книга 3"]
        for book in books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)
        assert collector.get_list_of_favorites_books() == books

    def test_get_list_of_favorites_books_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []

    #Комплексный тест
    def test_full_workflow(self, collector):
        collector.add_new_book("Война и мир")
        collector.add_new_book("Анна Каренина")
        collector.add_new_book("Мертвые души")

        collector.set_book_genre("Война и мир", "Комедия")
        collector.set_book_genre("Анна Каренина", "Фантастика")

        children_books = collector.get_books_for_children()
        assert "Война и мир" in children_books
        assert "Анна Каренина" in children_books
        assert "Мертвые души" not in children_books

        collector.add_book_in_favorites("Война и мир")
        collector.add_book_in_favorites("Анна Каренина")
        assert len(collector.get_list_of_favorites_books()) == 2

        collector.delete_book_from_favorites("Война и мир")
        favorites = collector.get_list_of_favorites_books()
        assert "Война и мир" not in favorites
        assert "Анна Каренина" in favorites

        assert collector.get_book_genre("Война и мир") == "Комедия"