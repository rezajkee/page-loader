import pytest
import tempfile
import os
import requests_mock
from page_loader import download
from page_loader.page_loader import KnownException


@pytest.mark.asyncio
async def test_no_access():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(
                "https://ru.hexlet.io/courses",
                text="hello",
            )
        os.chmod(tmpdirname, 000)
        with pytest.raises(KnownException):
            download("https://ru.hexlet.io/courses", tmpdirname)


@pytest.mark.asyncio
async def test_bad_http_status():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(
                "https://ru.hexlet.io/courses",
                status_code=404,
            )
            with pytest.raises(KnownException):
                download("https://ru.hexlet.io/courses", tmpdirname)
