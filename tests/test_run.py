import subprocess
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
import run_evaluation_pipeline as rep


def test_run_raises_on_bad_command():
    with pytest.raises(subprocess.CalledProcessError):
        rep.run(["false"])
