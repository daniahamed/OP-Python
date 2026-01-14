import pytest
from unittest.mock import MagicMock, patch

from src.controllers.user_c import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    get_user_book_count,
)

@patch("src.controllers.user_c.db")
@patch("src.controllers.user_c.User")
def test_create_user_success(mock_user_cls, mock_db):
    fake_user = MagicMock()
    mock_user_cls.return_value = fake_user

    result = create_user(" Alice ")

    mock_user_cls.assert_called_once_with(name="Alice")
    mock_db.session.add.assert_called_once_with(fake_user)
    mock_db.session.commit.assert_called_once()
    assert result == fake_user

@pytest.mark.parametrize("bad_name", ["", "   ", None, 123])
def test_create_user_invalid_name(bad_name):
    with pytest.raises(ValueError):
        create_user(bad_name)

@patch("src.controllers.user_c.User")
def test_get_all_users(mock_user):
    fake_users = [MagicMock(), MagicMock()]
    mock_user.query.all.return_value = fake_users

    result = get_all_users()

    assert result == fake_users

@patch("src.controllers.user_c.User")
def test_get_user_by_id_found(mock_user):
    fake_user = MagicMock()
    mock_user.query.get.return_value = fake_user

    result = get_user_by_id(1)

    assert result == fake_user

@patch("src.controllers.user_c.User")
def test_get_user_by_id_not_found(mock_user):
    mock_user.query.get.return_value = None

    with pytest.raises(ValueError):
        get_user_by_id(999)

@patch("src.controllers.user_c.db")
@patch("src.controllers.user_c.User")
def test_update_user_name(mock_user, mock_db):
    fake_user = MagicMock()
    mock_user.query.get.return_value = fake_user

    result = update_user(1, name=" Bob ")

    assert fake_user.name == "Bob"
    mock_db.session.commit.assert_called_once()
    assert result == fake_user

@patch("src.controllers.user_c.User")
def test_update_user_not_found(mock_user):
    mock_user.query.get.return_value = None

    with pytest.raises(ValueError):
        update_user(1, name="Bob")

@patch("src.controllers.user_c.db")
@patch("src.controllers.user_c.User")
def test_delete_user_success(mock_user, mock_db):
    fake_user = MagicMock()
    mock_user.query.get.return_value = fake_user

    delete_user(1)

    mock_db.session.delete.assert_called_once_with(fake_user)
    mock_db.session.commit.assert_called_once()

@patch("src.controllers.user_c.User")
def test_delete_user_not_found(mock_user):
    mock_user.query.get.return_value = None

    with pytest.raises(ValueError):
        delete_user(1)

@patch("src.controllers.user_c.User")
def test_get_user_book_count(mock_user):
    fake_user = MagicMock()
    fake_user.library.books = [1, 2, 3]

    mock_user.query.get.return_value = fake_user

    result = get_user_book_count(1)

    assert result == 3

@patch("src.controllers.user_c.User")
def test_get_user_book_count_no_library(mock_user):
    fake_user = MagicMock()
    fake_user.library = None

    mock_user.query.get.return_value = fake_user

    assert get_user_book_count(1) == 0

@patch("src.controllers.user_c.User")
def test_get_user_book_count_user_not_found(mock_user):
    mock_user.query.get.return_value = None

    with pytest.raises(ValueError):
        get_user_book_count(1)
