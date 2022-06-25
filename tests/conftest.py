import os
import pytest
import asyncio
import pytest_asyncio

FIXTURES_FOLDER = 'fixtures'


@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def hexlet_html_path():
    return os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'hexlet.html')


@pytest.fixture(scope='session')
def hexlet_html_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'hexlet.html')
    with open(path, "r") as f:
        return f.read()


@pytest.fixture(scope='session')
def nodejs_png_path():
    return os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'nodejs.png')


@pytest.fixture(scope='session')
def nodejs_png_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'nodejs.png')
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture(scope='session')
def application_css_path():
    return os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'application.css')


@pytest.fixture(scope='session')
def application_css_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'application.css')
    with open(path, "rb") as f:
        return f.read()


@pytest.fixture(scope='session')
def runtime_js_path():
    return os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'runtime.js')


@pytest.fixture(scope='session')
def runtime_js_read():
    path = os.path.join(os.path.dirname(__file__),
                        FIXTURES_FOLDER, 'runtime.js')
    with open(path, "rb") as f:
        return f.read()


@pytest_asyncio.fixture(scope='function')
async def result_html(request):
    assert getattr(request.module, 'FIXTURE_NAME', None)

    result_path = os.path.join(
        os.path.dirname(__file__), FIXTURES_FOLDER, request.module.FIXTURE_NAME)

    with open(result_path) as file:
        return file.read()
