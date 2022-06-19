import tempfile
import requests_mock
from page_loader.page_loader import get_html, make_name


def test_get_html():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with requests_mock.Mocker() as m:
            m.get("http://test.hello.com/any/try0me.php", text="Some data here")
            name_from_url = make_name("http://test.hello.com/any/try0me.php")
            new_file_path = get_html(
                "http://test.hello.com/any/try0me.php",
                tmpdirname,
                name_from_url,
            )
            with open(new_file_path, "r") as f:
                assert f.read().rstrip() == "Some data here"
                assert (
                    new_file_path
                    == tmpdirname + "/test-hello-com-any-try0me.html"
                )
