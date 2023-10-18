import pytest
from fastapi_mctools.exceptions import HTTPException, exception_handler


def test_http_exception_attributes():
    custom_exception = HTTPException(
        status_code=404,
        detail="Item not found",
        code="NOT_FOUND",
        headers={"Custom-Header": "Value"},
    )

    assert (
        custom_exception.status_code == 404
    ), f"Expected 404, got {custom_exception.status_code}"
    assert (
        custom_exception.detail == "Item not found"
    ), f"Expected 'Item not found', got {custom_exception.detail}"
    assert (
        custom_exception.code == "NOT_FOUND"
    ), f"Expected 'NOT_FOUND', got {custom_exception.code}"
    assert custom_exception.headers == {
        "Custom-Header": "Value"
    }, f"Expected {'Custom-Header': 'Value'}, got {custom_exception.headers}"


@pytest.mark.asyncio
async def test_exception_handler():
    exception = await exception_handler(Exception("Test exception"))
    assert exception.status_code == 500
    assert isinstance(exception, HTTPException)
