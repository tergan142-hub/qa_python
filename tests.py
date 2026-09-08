import pytest
from main import BooksCollector

class TestBooksCollector:

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
    #проверка set_book_genre
    def test_set_book_genre_atomic(self, collector):
        book_name = "Тестовая"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.get_book_genre(book_name) == "Фактастика"

    #проверка get_book_genre:
    def test_get_book_genre_atomic(self, collector):
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Фантастика")
        assert collector.get_book_genre("Книга 1") == "Фантастика"

        collector.add_new_book("Книга 2")
        assert collector.get_book_genre("Книга 2") == ""

        assert collector.get_book_genre("Несуществующая") is None

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
    @pytest.mark.parametrize("book_name", ["Масетр и Маргарита", "Преступление и наказание", "Собачье сердце"])
    def test_delete_book_from_favorites_success(self, collector, book_name):
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
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

#общая проверка
    #тесты для get_books_for_children
    def test_get_books_for_children_includes_allowed_genre_books(self, collector):
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Комедия")
        children_books = collector.get_books_for_children()
        assert "Война и мир" in children_books

    def test_get_books_for_children_excludes_horror_books(self, collector):
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        children_books = collector.get_books_for_children()
        assert "Оно" not in children_books

    def test_get_books_for_children_excludes_detective_books(self, collector):
        collector.add_new_book("Убийство в Восточном экспрессе")
        collector.set_book_genre("Убийство в Восточном экспрессе", "Детективы")
        children_books = collector.get_books_for_children()
        assert "Убийство в Восточном экспрессе" not in children_books

    def test_get_books_for_children_excludes_books_without_genre(self, collector):
        collector.add_new_book("Мертвые души")
        children_books = collector.get_books_for_children()
        assert "Мертвые души" not in children_books

    #тесты для add_book_in_favorites
    def test_add_book_in_favorites_increses_favorites_count(self, collector):
        collector.add_new_book("Война и мир")
        collector.add_new_book("Анна Каренина")
        assert len(collector.get_lis_of_favorites_books()) == 2

    def test_add_book_in_favorites_ignore_nonexistent_book(self, collector):
        collector.add_new_book_in_favorites("Несуществующая")
        assert len(collector.get_list_of_favorites_books()) == 0

    #тесты для delete_book_from_favorites
    def test_delete_book_fron_favorites_removes_specific_book(self, collector):
        collector.add_new_book("Война и мир")
        collector.add_book_in_favorites("Война и мир")
        collector.add_new_book("Анна Каренина")
        collector.add_book_in_favorites("Анна Каренина")
        collector.delete_book_from_favorites("Война и мир")
        assert "Война и мир" not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_keeps_other_favorites(self, collector):
        collector.add_new_book("Война и мир")
        collector.add_book_in_favorites("Война и мир")
        collector.add_new_book("Анна Каренина")
        collector.add_book_in_favorites("Анна Каренина")
        collector.delete_book_from_favorites("Война и мир")
        assert "Анна Каренина" in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites_handles_non_favorite_book(self, collector):
        collector.add_new_book("Война и мир")
        collector.delete_book_from_favorites("Война и мир")
        assert collector.get_list_of_favorites_books() == []

    #тесты для get_book_genre
    def test_get_book_genre_persists_after_favorites_operations(self, collector):
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Комедия")
        collector.add_new_book_in_favorites("Война и мир")
        collector.delete_book_from_favorites("Война и мир")
        assert collector.get_book_genre("Война и мир") == "Комедия"

    def test_get_book_genre_unchanged_after_adding_to_favorites(self, collector):
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Комедия")
        collector.add_book_in_favorites("Война и мир")
        assert collector.get_book_genre("Война и мир") == "Комедия"

    def test_get_book_genre_unchanged_after_deleting_from_favorites(self, collector):
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Комедия")
        collector.add_book_in_favorites("Война и мир")
        collector.delete_book_from_favorites("Война и мир")
        assert collector.get_book_genre("Война и мир") == "Комедия"