import pytest
from unittest.mock import MagicMock, patch

from src.controllers.library_c import (
    create_library,
    get_all_libraries,
    get_library_by_id,
    update_library,
    delete_library,
)

# Create library
@patch("src.controllers.library_c.db")
@patch("src.controllers.library_c.Library")
@patch("src.controllers.library_c.User")
def test_create_library_success(mock_user, mock_library_cls, mock_db):
    fake_owner = MagicMock()
    fake_library = MagicMock(id=1)

    mock_user.query.get.return_value = fake_owner
    mock_library_cls.query.filter_by.return_value.first.return_value = None
    mock_library_cls.return_value = fake_library

    result = create_library(" My Library ", owner_id=10)

    mock_library_cls.assert_called_once_with(name="My Library", owner_id=10)
    mock_db.session.add.assert_called_once_with(fake_library)
    mock_db.session.commit.assert_called_once()
    assert result == fake_library

# Owner doesn't exist
@patch("src.controllers.library_c.User")
def test_create_library_owner_not_found(mock_user):
    mock_user.query.get.return_value = None

    with pytest.raises(ValueError):
        create_library("Library", owner_id=1)


# Owner already has a library
@patch("src.controllers.library_c.Library")
@patch("src.controllers.library_c.User")
def test_create_library_owner_already_has_library(mock_user, mock_library):
    fake_owner = MagicMock()
    existing_library = MagicMock(id=99)

    mock_user.query.get.return_value = fake_owner
    mock_library.query.filter_by.return_value.first.return_value = existing_library

    with pytest.raises(ValueError):
        create_library("Library", owner_id=1)

# Invalid name
@pytest.mark.parametrize("bad_name", ["", "   ", None, 123])
def test_create_library_invalid_name(bad_name):
    with pytest.raises(ValueError):
        create_library(bad_name, owner_id=1)


# Get all
@patch("src.controllers.library_c.Library")
def test_get_all_libraries(mock_library):
    fake_libraries = [MagicMock(), MagicMock()]
    mock_library.query.all.return_value = fake_libraries

    result = get_all_libraries()

    assert result == fake_libraries

# Get by id
@patch("src.controllers.library_c.Library")
def test_get_library_by_id_found(mock_library):
    fake_library = MagicMock()
    mock_library.query.get.return_value = fake_library

    result = get_library_by_id(1)

    assert result == fake_library

#notfound
@patch("src.controllers.library_c.Library")
def test_get_library_by_id_not_found(mock_library):
    mock_library.query.get.return_value = None

    with pytest.raises(ValueError):
        get_library_by_id(999)

# update name
@patch("src.controllers.library_c.db")
@patch("src.controllers.library_c.Library")
def test_update_library_name(mock_library, mock_db):
    fake_library = MagicMock()
    mock_library.query.get.return_value = fake_library

    result = update_library(1, name=" New Name ")

    assert fake_library.name == "New Name"
    mock_db.session.commit.assert_called_once()
    assert result == fake_library

# library not found
@patch("src.controllers.library_c.Library")
def test_update_library_not_found(mock_library):
    mock_library.query.get.return_value = None

    with pytest.raises(ValueError):
        update_library(1, name="Test")

# update owner 
@patch("src.controllers.library_c.db")
@patch("src.controllers.library_c.Library")
@patch("src.controllers.library_c.User")
def test_update_library_owner(mock_user, mock_library, mock_db):
    fake_library = MagicMock(id=1)
    fake_owner = MagicMock()

    mock_library.query.get.return_value = fake_library
    mock_user.query.get.return_value = fake_owner
    mock_library.query.filter_by.return_value.first.return_value = None

    result = update_library(1, owner_id=2)

    assert fake_library.owner_id == 2
    mock_db.session.commit.assert_called_once()
    assert result == fake_library


# owner already has a library
@patch("src.controllers.library_c.Library")
@patch("src.controllers.library_c.User")
def test_update_library_owner_already_has_library(mock_user, mock_library):
    fake_library = MagicMock(id=1)
    fake_owner = MagicMock()
    existing_library = MagicMock(id=2)

    mock_library.query.get.return_value = fake_library
    mock_user.query.get.return_value = fake_owner
    mock_library.query.filter_by.return_value.first.return_value = existing_library

    with pytest.raises(ValueError):
        update_library(1, owner_id=2)

# Delete library
@patch("src.controllers.library_c.db")
@patch("src.controllers.library_c.Library")
def test_delete_library_success(mock_library, mock_db):
    fake_library = MagicMock()
    mock_library.query.get.return_value = fake_library

    result = delete_library(1)

    mock_db.session.delete.assert_called_once_with(fake_library)
    mock_db.session.commit.assert_called_once()
    assert result is True

# not found
@patch("src.controllers.library_c.Library")
def test_delete_library_not_found(mock_library):
    mock_library.query.get.return_value = None

    with pytest.raises(ValueError):
        delete_library(1)
