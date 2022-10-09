import os
import tempfile

import pytest
import requests_mock
from page_loader.file_actions import create_directory, save_content
from page_loader.page_loader import KnownException, download


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


@pytest.mark.asyncio
async def test_create_dir_no_access():
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.chmod(tmpdirname, 000)
        with pytest.raises(KnownException):
            create_directory("https://ru.hexlet.io/courses", tmpdirname)


@pytest.mark.asyncio
async def test_save_cont_bad_http_status():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(
                "https://ru.hexlet.io/courses",
                status_code=404,
            )
            with pytest.raises(KnownException):
                save_content("https://ru.hexlet.io/courses", tmpdirname)


@pytest.mark.asyncio
async def test_save_cont_no_access():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(
                "https://ru.hexlet.io/courses",
                text="hello",
            )
        os.chmod(tmpdirname, 000)
        with pytest.raises(KnownException):
            save_content(
                "https://ru.hexlet.io/courses",
                os.path.join(tmpdirname, "content"),
            )
