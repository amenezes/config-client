from config import http


def test_get():
    resp = http.get("https://httpbin.org/get")
    assert resp.ok


def test_post():
    resp = http.post("https://httpbin.org/post")
    assert resp.ok
