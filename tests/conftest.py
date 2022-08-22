import os
import pytest
import asyncio

FIXTURES_FOLDER = 'fixtures'


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def hexlet_html_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'hexlet.html')
    with open(path, "r") as f:
        return f.read()


@pytest.fixture(scope='session')
def no_tags_html_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'no_tags.html')
    with open(path, "r") as f:
        return f.read()


@pytest.fixture(scope='session')
def nodejs_png_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'nodejs.png')
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture(scope='session')
def application_css_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'application.css')
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture(scope='session')
def noexe_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'noexe')
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture(scope='session')
def runtime_js_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'runtime.js')
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture(scope='session')
def hexlet_result_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'hexlet_result.html')
    with open(path, "r") as f:
        return f.read()


@pytest.fixture(scope='session')
def no_tags_result_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'no_tags_result.html')
    with open(path, "r") as f:
        return f.read()
