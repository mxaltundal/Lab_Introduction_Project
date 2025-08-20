import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
import download_hg002_giab as dl


def test_download_file_skips_existing(tmp_path, monkeypatch, caplog):
    filename = "dummy.txt"
    dest = tmp_path / filename
    dest.write_text("existing")

    def fake_urlretrieve(url, dest_path):
        raise AssertionError("urlretrieve should not be called for existing files")

    monkeypatch.setattr(dl, "urlretrieve", fake_urlretrieve)

    file_info = {"name": filename, "md5": "", "sha256": ""}
    with caplog.at_level("INFO"):
        dl.download_file(file_info, str(tmp_path))
    assert "[skip]" in caplog.text
