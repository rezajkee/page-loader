import tempfile
import requests_mock
from page_loader.page_loader import dwl_pics_mod_html, make_name, make_dir
import shutil
import os


def test_get_pics():
    with tempfile.TemporaryDirectory() as tmpdirname:
        copyed_html = shutil.copy('/home/rezajkee/study/projects/python-project-lvl3/tests/fixtures/hexlet.html', tmpdirname)
        with requests_mock.Mocker() as m:
            m.get('https://ru.hexlet.io/assets/professions/nodejs.png', text='Some data here')
            name_from_url = make_name('https://ru.hexlet.io/courses')
            assert name_from_url == 'ru-hexlet-io-courses'
            dir_abs_path = make_dir(name_from_url, tmpdirname)
            assert os.path.isdir(dir_abs_path)
            dwl_pics_mod_html(
                'https://ru.hexlet.io/courses', copyed_html, dir_abs_path
            )
            assert os.path.isfile(os.path.join(dir_abs_path, "ru-hexlet-io-assets-professions-nodejs.png"))
            with open(copyed_html, "r") as f:
                with open('/home/rezajkee/study/projects/python-project-lvl3/tests/fixtures/hexlet_pic.html', "r") as r:
                    assert f.read() == r.read()

