import sys
from pathlib import Path

import main as app


def test_create_directory_creates_missing_directory(tmp_path):
    target = tmp_path / "nested" / "qr_codes"

    app.create_directory(target)

    assert target.exists()
    assert target.is_dir()


def test_is_valid_url_accepts_valid_url():
    assert app.is_valid_url("https://github.com/anutale") is True


def test_is_valid_url_rejects_invalid_url(caplog):
    result = app.is_valid_url("not-a-valid-url")

    assert result is False
    assert "Invalid URL provided" in caplog.text


def test_generate_qr_code_saves_png_for_valid_url(tmp_path):
    output_path = tmp_path / "sample.png"

    app.generate_qr_code("https://example.com", output_path, "black", "white")

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_generate_qr_code_ignores_invalid_url(tmp_path):
    output_path = tmp_path / "invalid.png"

    app.generate_qr_code("not-a-valid-url", output_path, "black", "white")

    assert not output_path.exists()


def test_main_generates_qr_code_from_cli(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["main.py", "--url", "https://example.com"])

    app.main()

    qr_dir = tmp_path / app.QR_DIRECTORY
    files = list(qr_dir.glob("QRCode_*.png"))
    assert qr_dir.exists()
    assert len(files) == 1
    assert files[0].stat().st_size > 0
