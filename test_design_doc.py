from pathlib import Path

DESIGN_DOC = Path(__file__).parent / "docs" / "design" / "MYW-13-calendar-telegram-agent.md"

REQUIRED_SECTIONS = [
    "## 1. Цель и контекст",
    "## 2. Требования",
    "## 3. Архитектура верхнего уровня",
    "## 4. Компоненты",
    "## 5. Основной сценарий",
    "## 6. Обработка ошибок",
    "## 7. Безопасность",
    "## 8. Технологический стек",
    "## 9. План поэтапной реализации",
    "## 10. Открытые вопросы",
]


def test_design_doc_exists():
    assert DESIGN_DOC.is_file(), f"missing design doc: {DESIGN_DOC}"


def test_design_doc_has_required_sections():
    text = DESIGN_DOC.read_text(encoding="utf-8")
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    assert not missing, f"design doc is missing sections: {missing}"


def test_readme_links_to_design_doc():
    readme = Path(__file__).parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert "docs/design/MYW-13-calendar-telegram-agent.md" in text
