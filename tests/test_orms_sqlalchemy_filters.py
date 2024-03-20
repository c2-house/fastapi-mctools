import pytest
from fastapi_mctools.orms.sqlalchemy.filters import FilterBackend


class TestFilterBackend:
    @pytest.fixture
    def filter_backend(self):
        return FilterBackend()

    @pytest.fixture
    def mock_model(self, mocker):
        model = mocker.MagicMock()
        model.name = "James"
        model.age = 25
        return model

    def test_add_filter(self, filter_backend, mock_model):
        filter_backend.set_model(mock_model)
        condition = {"name": "James"}
        operator = "eq"
        filter_backend.add_filter(condition, operator)

        assert len(filter_backend.filters) == 1

    def test_compile_single_filter(self, filter_backend, mock_model):
        filter_backend.set_model(mock_model)
        condition = {"name": "James"}
        operator = "eq"
        filter_backend.add_filter(condition, operator)

        compiled_filter = filter_backend.compile()

        assert compiled_filter is not None

    def test_compile_multiple_filters(self, filter_backend, mock_model):
        filter_backend.set_model(mock_model)
        condition1 = {"name": "James"}
        operator1 = "eq"
        filter_backend.add_filter(condition1, operator1)

        condition2 = {"age": 25}
        operator2 = "gt"
        filter_backend.add_filter(condition2, operator2)

        compiled_filter = filter_backend.compile()

        assert compiled_filter is not None

    def test_compile_no_filters(self, filter_backend: FilterBackend):
        with pytest.raises(ValueError):
            filter_backend.compile()
