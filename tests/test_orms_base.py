import pytest
from fastapi_mctools.orms import ORMBase


@pytest.fixture(name="MockModel")
def MockModel():
    class _MockModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    return _MockModel


def test_orm_base_get_columns(MockModel):
    mock_model = MockModel
    mock_model.column1 = "value1"
    mock_model.column2 = "value2"
    orm_base = ORMBase(mock_model)
    columns = ["column1", "column2"]
    result = orm_base.get_columns(columns)
    assert len(result) == 2
    assert result[0] == getattr(MockModel, "column1")
    assert result[1] == getattr(MockModel, "column2")


def test_orm_base_get_columns_all(MockModel):
    orm_base = ORMBase(MockModel)
    result = orm_base.get_columns()
    assert len(result) == 1
    assert result[0] == MockModel


def test_orm_base_get_result(MockModel, mocker):
    orm_base = ORMBase(MockModel)
    result = mocker.MagicMock()
    columns = ["column1"]
    result.scalar_one_or_none.return_value = "result_value"
    assert orm_base.get_result(result, columns) == "result_value"
    result.scalar_one_or_none.assert_called_once()


def test_orm_base_get_result_all(MockModel, mocker):
    orm_base = ORMBase(MockModel)
    result = mocker.MagicMock()
    columns = ["column1", "column2"]
    result.mappings().first.return_value = "result_value"
    assert orm_base.get_result(result, columns) == "result_value"
    result.mappings().first.assert_called_once()


def test_orm_base_get_results(MockModel, mocker):
    orm_base = ORMBase(MockModel)
    results = mocker.MagicMock()
    columns = ["column1"]
    results.scalars().all.return_value = ["result_value"]
    assert orm_base.get_results(results, columns) == ["result_value"]
    results.scalars().all.assert_called_once()


def test_orm_base_get_results_all(MockModel, mocker):
    orm_base = ORMBase(MockModel)
    results = mocker.MagicMock()
    columns = ["column1", "column2"]
    results.mappings().all.return_value = ["result_value"]
    assert orm_base.get_results(results, columns) == ["result_value"]
    results.mappings().all.assert_called_once()


def test_orm_base_get_filters_by_operator(MockModel):
    orm_base = ORMBase(MockModel)
    orm_base.model.key1 = "value1"
    orm_base.model.key2 = "value2"
    kwargs = {"key1": "value1", "key2": "value2"}
    operator = "eq"
    result = orm_base.get_filters_by_operator(kwargs, operator)
    assert len(result) == 2
    assert result[0] == (getattr(MockModel, "key1") == "value1")
    assert result[1] == (getattr(MockModel, "key2") == "value2")


def test_orm_base_get_filters_by_operator_invalid_key(MockModel):
    orm_base = ORMBase(MockModel)
    kwargs = {"invalid_key": "value"}
    operator = "eq"
    result = orm_base.get_filters_by_operator(kwargs, operator)
    assert len(result) == 0


def test_orm_base_get_filters_by_operator_invalid_operator(MockModel):
    orm_base = ORMBase(MockModel)
    with pytest.raises(ValueError):
        kwargs = {"key": "value"}
        operator = "invalid_operator"
        orm_base.get_filters_by_operator(kwargs, operator)
