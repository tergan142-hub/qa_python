# qa_python
test_add_new_book_success - проверка успешного добавление новой книги в коллекцию
test_add_new_book_invalid_lenght - проверка недопустимости длинного названия
test_add_new_book_duplicate - проверка, что дубликат книги не создается
test_set_book_genre_success - проверка установки жарка книги
test_set_book_genre_book_not_exists - проверка того, что невозможно установить жанр для несуществующей книги
test_set_book_genre_existing_book - проверка получения жанра несуществующей книги
test_get_book_genre_no genre_set - проверка получения жанра книги без установленного жанра книги
test_get_books_with_specific_genre - проверка получения книг с определенным жанром
test_get_books_with_specific_genre_empty - проверка получения книг с жанром, которого нет
test_get_books_genre_returns_dict - проверка, что методы возвращает словарь с книгами и жанрами
test_get_books_genre_empty - проверка возвращения пустого словаря с книгами и жанрами
test_get_books_for_children_mixed_genre - проверка получения детских книг с разными жанрами
test_get_books_for_children_empty - проверка, что книги со взрослыми жанрами не попадают в детский список
test_get_books_for_children_no_books - проверка получения дестких книг при их отсутствии в коллекции
test_add_book_in_favorites_success - проверка добавлени книги в избранное
test_add_book_in_favorites_not_in_books_genre - проверка невозможности добавить книгу в избранное, которой нет в списке
test_add_book_in_favorites_duplicate - проверка того, что дубликат не добавляется в избранное
test_add_book_in_favorites_without_genre - проверка того, что нельзя добавить в избранное книгу без жанра
test_delete_book_form_favorites_success - проверка удаления книги из избранного
test_delete_book_form_favorites_not_in_favorites - проверка удаления книги, которой нет в избранном
test_delete_book_form_favorites_not_in_books_genre - проверка удаления несуществующей книги из избранного
test_get_list_of_favorites_books_with_books - проверка получения списка избранных книг при наличии книг
test_get_list_of_favorites_books_empty - проверка получения списка книг из избранного, при условии пустого избранного
test_full_workflow - комплексный тест, проверка рабочих процессов