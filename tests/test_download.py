import tempfile
import requests_mock
from page_loader import download


def test_download():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get('http://test.hello.com/any/try0me.php', text='Some data here')
            new_file_path = download(
                'http://test.hello.com/any/try0me.php', tmpdirname
            )
            with open(new_file_path, "r") as f:
                assert f.read().rstrip() == 'Some data here'
                assert new_file_path == tmpdirname + "/test-hello-com-any-try0me.html"
