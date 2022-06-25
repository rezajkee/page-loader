import pytest
import tempfile
import requests_mock
import os
from page_loader import download

FIXTURE_NAME = "hexlet_result.html"


@pytest.mark.asyncio
async def test_download(
    hexlet_html_read,
    application_css_read,
    nodejs_png_read,
    runtime_js_read,
    result_html,
):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get(
                "https://ru.hexlet.io/courses",
                text=hexlet_html_read,
            )
            m.get(
                "/assets/application.css",
                content=application_css_read,
            )
            m.get(
                "/assets/professions/nodejs.png",
                content=nodejs_png_read,
            )
            m.get(
                "https://ru.hexlet.io/packs/js/runtime.js",
                content=runtime_js_read,
            )
            path_to_html = download("https://ru.hexlet.io/courses", tmpdirname)
            with open(path_to_html, "r") as f1:
                assert f1.read() == result_html
            with open(
                os.path.join(
                    tmpdirname,
                    "ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css",  # noqa: E501
                ),
                "rb",
            ) as f2:
                assert f2.read() == application_css_read
            with open(
                os.path.join(
                    tmpdirname,
                    "ru-hexlet-io-courses_files/ru-hexlet-io-courses.html",
                ),
                "r",
            ) as f3:
                assert f3.read() == hexlet_html_read
            with open(
                os.path.join(
                    tmpdirname,
                    "ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png",  # noqa: E501
                ),
                "rb",
            ) as f4:
                assert f4.read() == nodejs_png_read
            with open(
                os.path.join(
                    tmpdirname,
                    "ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js",  # noqa: E501
                ),
                "rb",
            ) as f5:
                assert f5.read() == runtime_js_read
