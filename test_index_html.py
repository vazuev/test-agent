from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def parse():
    c = Collector()
    c.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return c.tags


def test_lang_and_charset_and_viewport():
    tags = parse()
    assert ("html", {"lang": "ru"}) in tags
    assert any(t == "meta" and a.get("charset", "").lower() == "utf-8" for t, a in tags)
    assert any(t == "meta" and a.get("name") == "viewport" for t, a in tags)


def test_single_native_button_with_label():
    tags = parse()
    assert [t for t, _ in tags].count("button") == 1
    assert "Нажми на меня" in (ROOT / "index.html").read_text(encoding="utf-8")


def test_message_area_is_live_and_initially_empty():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert "Добрый вечер" not in html
    assert any(a.get("aria-live") == "polite" for _, a in parse())


def test_script_sets_message_without_duplicating():
    js = (ROOT / "script.js").read_text(encoding="utf-8")
    assert "Добрый вечер" in js
    assert "textContent =" in js
    assert "appendChild" not in js and "+=" not in js
