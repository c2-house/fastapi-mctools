import pytest
import asyncio
from fastapi_mctools.utils.time import time_checker
from unittest.mock import MagicMock


class TestTimeChecker:
    @pytest.fixture
    def mock_logger(self, mocker):
        return mocker.MagicMock()

    @pytest.mark.asyncio
    async def test_time_checker_decorator(self, mock_logger: MagicMock):
        @time_checker(debug=True, logger=mock_logger)
        class TestClass:
            def __init__(self):
                pass

            async def test_method(self):
                await asyncio.sleep(0.01)

        instance = TestClass()
        await instance.test_method()

        mock_logger.info.assert_called_once()

    def test_time_checker_decorator_no_logger(self):
        with pytest.raises(AttributeError):

            @time_checker(debug=True)
            class TestClass:
                def __init__(self):
                    pass

                async def test_method(self):
                    await asyncio.sleep(0.01)

    @pytest.mark.asyncio
    async def test_time_checker_decorator_no_debug(self, mock_logger: MagicMock):
        @time_checker(logger=mock_logger)
        class TestClass:
            def __init__(self):
                pass

            async def test_method(self):
                await asyncio.sleep(0.01)

        instance = TestClass()
        await instance.test_method()

        mock_logger.info.assert_not_called()
