import pytest
from sqlalchemy.orm import Session
from fastapi_mctools.orms.sqlalchemy.sync_base import (
    CreateBase,
    ReadBase,
    UpdateBase,
    DeleteBase,
)


@pytest.fixture(scope="session", name="MockModel")
def MockModel():
    class _MockModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    return _MockModel


def test_create_base(MockModel, mocker):
    session = mocker.MagicMock(spec=Session)
    create_base = CreateBase(MockModel)

    create_base.create(session, key1="value1", key2="value2")
    session.add.assert_called()
    session.commit.assert_called()
    session.refresh.assert_called()


def test_read_base_get(MockModel, mocker):
    mock_session = mocker.MagicMock(spec=Session)
    read_base = ReadBase(MockModel)
    read_base.model.id = 1

    mock_query = mocker.MagicMock()
    mock_session.query.return_value = mock_query

    read_base.get(mock_session, 1)

    mock_session.query.assert_called_with(MockModel)
    mock_query.filter.assert_called_once()


def test_read_base_get_by_filters(MockModel, mocker):
    mock_session = mocker.MagicMock(spec=Session)
    read_base = ReadBase(MockModel)

    mock_query = mocker.MagicMock()
    mock_session.query.return_value = mock_query

    read_base.get_by_filters(mock_session, key="value")

    mock_session.query.assert_called_with(MockModel)
    mock_query.filter.assert_called_once()


def test_read_base_get_all(MockModel, mocker):
    mock_session = mocker.MagicMock(spec=Session)
    read_base = ReadBase(MockModel)

    mock_query = mocker.MagicMock()
    mock_session.query.return_value = mock_query

    read_base.get_all(mock_session)

    mock_session.query.assert_called_with(MockModel)
    mock_query.all.assert_called_once()


def test_read_base_get_all_by_filters(MockModel, mocker):
    mock_session = mocker.MagicMock(spec=Session)
    read_base = ReadBase(MockModel)

    mock_query = mocker.MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_query

    read_base.get_all_by_filters(mock_session, key="value")

    mock_session.query.assert_called_with(MockModel)
    mock_query.filter.assert_called_once()
    mock_query.all.assert_called_once()


def test_update_base_by_obj(MockModel, mocker):
    mock_session = mocker.MagicMock(spec=Session)
    update_base = UpdateBase(MockModel)

    mock_db_obj = mocker.MagicMock()

    kwargs = {"key1": "value1", "key2": "value2"}

    result = update_base.update_by_obj(mock_session, mock_db_obj, **kwargs)

    for key, value in kwargs.items():
        setattr(mock_db_obj, key, value)

    mock_session.commit.assert_called_once()

    mock_session.refresh.assert_called_once_with(mock_db_obj)

    assert result == mock_db_obj


def test_delete_base(MockModel, mocker):
    mock_session = mocker.MagicMock(spec=Session)
    delete_base = DeleteBase(MockModel)

    mock_db_obj = mocker.MagicMock()

    result = delete_base.delete(mock_session, mock_db_obj)

    mock_session.delete.assert_called_once_with(mock_db_obj)

    mock_session.commit.assert_called_once()

    assert result == mock_db_obj
