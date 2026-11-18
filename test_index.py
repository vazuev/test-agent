import pathlib

html = pathlib.Path("index.html").read_text(encoding="utf-8")


def test_single_canvas_no_greeting_no_deps():
    assert html.count("<canvas") == 1
    assert "Привет" not in html
    assert "src=" not in html


def test_compact():
    assert len(html.strip().splitlines()) <= 25


def test_two_clouds_sun_sky_meadow():
    assert "#87ceeb" in html and "#4caf50" in html and "#ffd700" in html
    assert "[[90, 70], [220, 110]]" in html
