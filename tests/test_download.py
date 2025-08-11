import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
import download_hg002_giab as dl


def test_download_file_skips_existing(tmp_path, monkeypatch, capsys):
    filename = "dummy.txt"
    dest = tmp_path / filename
    dest.write_text("existing")

    def fake_urlretrieve(url, dest_path):
        raise AssertionError("urlretrieve should not be called for existing files")

    monkeypatch.setattr(dl, "urlretrieve", fake_urlretrieve)

    dl.download_file(filename, str(tmp_path))
    captured = capsys.readouterr().out
    assert "[skip]" in captured
