import pytest
from unittest.mock import MagicMock, patch

from src.controllers.book_c import (
    get_books,
    get_book_by_id,
    create_book,
    update_book,
    delete_book,
    transfer_book,
)

# get books
@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_get_books_filters(mock_library, mock_book):
    fake_query = MagicMock()
    mock_book.query = fake_query

    # simulate filter calls returning self
    fake_query.filter.return_value = fake_query
    fake_query.filter_by.return_value = fake_query
    fake_query.all.return_value = ["book1", "book2"]

    # library exists
    mock_library.query.get.return_value = True

    result = get_books(author="John", title="Python", library_id=1)

    assert result == ["book1", "book2"]
    fake_query.filter.assert_called()  
    fake_query.filter_by.assert_called_with(library_id=1)

# get book by id
@patch("src.controllers.book_c.Book")
def test_get_book_by_id_found(mock_book):
    fake_book = MagicMock()
    mock_book.query.get.return_value = fake_book

    result = get_book_by_id(1)
    assert result == fake_book


# not found
@patch("src.controllers.book_c.Book")
def test_get_book_by_id_not_found(mock_book):
    mock_book.query.get.return_value = None

    with pytest.raises(ValueError):
        get_book_by_id(999)

# create 
@patch("src.controllers.book_c.db")
@patch("src.controllers.book_c.Library")
@patch("src.controllers.book_c.Book")
def test_create_book_success(mock_book_cls, mock_library, mock_db):
    fake_library = MagicMock(id=1)
    fake_book = MagicMock(id=10)

    mock_library.query.get.return_value = fake_library
    mock_book_cls.return_value = fake_book

    result = create_book("Python 101", "John Doe", library_id=1)

    mock_book_cls.assert_called_once_with(title="Python 101", author="John Doe", library_id=1)
    mock_db.session.add.assert_called_once_with(fake_book)
    mock_db.session.commit.assert_called_once()
    assert result == fake_book


@patch("src.controllers.book_c.Library")
def test_create_book_library_not_found(mock_library):
    mock_library.query.get.return_value = None

    with pytest.raises(ValueError):
        create_book("Title", "Author", library_id=999)

@patch("src.controllers.book_c.Library")
def test_create_book_invalid_title(mock_library):
    mock_library.query.get.return_value = MagicMock()
    for bad_title in [None, "", "   ", 123]:
        with pytest.raises(ValueError):
            create_book(bad_title, "Author", library_id=1)


@patch("src.controllers.book_c.Library")
def test_create_book_long_title(mock_library):
    mock_library.query.get.return_value = MagicMock()
    long_title = "A" * 151
    with pytest.raises(ValueError):
        create_book(long_title, "Author", library_id=1)


@patch("src.controllers.book_c.Library")
def test_create_book_invalid_author(mock_library):
    mock_library.query.get.return_value = MagicMock()
    for bad_author in [None, "", "   ", 123]:
        with pytest.raises(ValueError):
            create_book("Title", bad_author, library_id=1)


@patch("src.controllers.book_c.Library")
def test_create_book_long_author(mock_library):
    mock_library.query.get.return_value = MagicMock()
    long_author = "A" * 101
    with pytest.raises(ValueError):
        create_book("Title", long_author, library_id=1)


@patch("src.controllers.book_c.Library")
def test_create_book_missing_library(mock_library):
    mock_library.query.get.return_value = None
    with pytest.raises(ValueError):
        create_book("Title", "Author", library_id=999)



# update book
@patch("src.controllers.book_c.db")
@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_update_book_all_fields(mock_library, mock_book, mock_db):
    fake_book = MagicMock(id=1)
    fake_library = MagicMock(id=2)

    mock_book.query.get.return_value = fake_book
    mock_library.query.get.return_value = fake_library

    result = update_book(1, title="New Title", author="New Author", library_id=2)

    assert fake_book.title == "New Title"
    assert fake_book.author == "New Author"
    assert fake_book.library_id == 2
    mock_db.session.commit.assert_called_once()
    assert result == fake_book

@patch("src.controllers.book_c.Book")
def test_update_book_not_found(mock_book):
    mock_book.query.get.return_value = None
    with pytest.raises(ValueError):
        update_book(1, title="New Title")


@patch("src.controllers.book_c.Book")
def test_update_book_invalid_title(mock_book):
    fake_book = MagicMock()
    mock_book.query.get.return_value = fake_book
    for bad_title in ["", "   ", 123]:
        with pytest.raises(ValueError):
            update_book(1, title=bad_title)


@patch("src.controllers.book_c.Book")
def test_update_book_long_title(mock_book):
    fake_book = MagicMock()
    mock_book.query.get.return_value = fake_book
    long_title = "A" * 151
    with pytest.raises(ValueError):
        update_book(1, title=long_title)


@patch("src.controllers.book_c.db")
@patch("src.controllers.book_c.Book")
def test_update_book_invalid_author(mock_book, mock_db):
    fake_book = MagicMock()
    mock_book.query.get.return_value = fake_book
    mock_db.session.commit = MagicMock() 

    for bad_author in [ "", "   "]:
        with pytest.raises(ValueError):
            update_book(1, author=bad_author)


@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_update_book_library_not_found(mock_library, mock_book):
    fake_book = MagicMock()
    mock_book.query.get.return_value = fake_book
    mock_library.query.get.return_value = None
    with pytest.raises(ValueError):
        update_book(1, library_id=999)


# delete book
@patch("src.controllers.book_c.db")
@patch("src.controllers.book_c.Book")
def test_delete_book_success(mock_book, mock_db):
    fake_book = MagicMock()
    mock_book.query.get.return_value = fake_book

    result = delete_book(1)

    mock_db.session.delete.assert_called_once_with(fake_book)
    mock_db.session.commit.assert_called_once()
    assert result is True


@patch("src.controllers.book_c.Book")
def test_delete_book_not_found(mock_book):
    mock_book.query.get.return_value = None

    with pytest.raises(ValueError):
        delete_book(1)

# transfer book
@patch("src.controllers.book_c.db")
@patch("src.controllers.book_c.Library")
@patch("src.controllers.book_c.Book")
def test_transfer_book_success(mock_book, mock_library, mock_db):
    fake_book = MagicMock(id=1, library_id=1)
    fake_library = MagicMock(id=2)

    mock_book.query.get.return_value = fake_book
    mock_library.query.get.return_value = fake_library

    result = transfer_book(1, 2)

    assert fake_book.library_id == 2
    mock_db.session.commit.assert_called_once()
    assert result == fake_book


@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_transfer_book_library_not_found(mock_library, mock_book):
    mock_book.query.get.return_value = MagicMock()
    mock_library.query.get.return_value = None

    with pytest.raises(ValueError):
        transfer_book(1, 999)

@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_transfer_book_no_target_library(mock_library, mock_book):
    with pytest.raises(ValueError):
        transfer_book(1, None)


@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_transfer_book_book_not_found(mock_library, mock_book):
    mock_book.query.get.return_value = None
    mock_library.query.get.return_value = MagicMock()
    with pytest.raises(ValueError):
        transfer_book(999, 1)


@patch("src.controllers.book_c.Book")
@patch("src.controllers.book_c.Library")
def test_transfer_book_library_not_found(mock_library, mock_book):
    mock_book.query.get.return_value = MagicMock()
    mock_library.query.get.return_value = None
    with pytest.raises(ValueError):
        transfer_book(1, 999)



