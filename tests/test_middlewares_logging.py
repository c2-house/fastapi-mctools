import logging
import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from fastapi_mctools.middlewares.logging import RequestLoggingMiddleware


@pytest.fixture
def test_app():
    app = FastAPI()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test_logger")

    app.add_middleware(
        RequestLoggingMiddleware,
        logger=logger,
        health_check_path="/health",
        tz_location="Asia/Seoul",
        allowed_hosts=["testserver"],
    )
    return app


@pytest.mark.asyncio
async def test_middleware_logs_properly(test_app, caplog):
    caplog.set_level(logging.INFO)

    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://testserver") as ac:
        response = await ac.get("/some_path")
        assert response.status_code == 404

    assert "some_path" in caplog.text
    assert "GET" in caplog.text
    assert "404" in caplog.text


@pytest.mark.asyncio
async def test_middleware_logs_capture_query_params(test_app, caplog):
    caplog.set_level(logging.INFO)

    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://testserver") as ac:
        response = await ac.get("/some_path?param1=1&param2=2")
        assert response.status_code == 404

    assert "param1=1" in caplog.text
    assert "param2=2" in caplog.text
