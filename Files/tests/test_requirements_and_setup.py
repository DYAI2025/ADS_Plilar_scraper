from pathlib import Path


def test_run_setup_uses_venv_and_requirements():
    content = Path("run_setup.sh").read_text(encoding="utf-8")
    assert "python3 -m venv .venv" in content
    assert "source .venv/bin/activate" in content
    assert "pip install -r requirements.txt" in content


def test_requirements_exists_and_core_packages():
    p = Path("requirements.txt")
    assert p.exists(), "requirements.txt fehlt"
    txt = p.read_text(encoding="utf-8")
    for pkg in ["pytest", "pandas", "jinja2"]:
        assert pkg in txt, f"{pkg} fehlt in requirements.txt"
