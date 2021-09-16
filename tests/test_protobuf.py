# -*- coding: utf-8 -*-
"""Integration test plugin."""
import tempfile
from pathlib import Path

from click.testing import CliRunner
from mkdocs.__main__ import build_command


def test_basic_working() -> None:
    """Run mkdocs and assert correct template parameters."""
    runner = CliRunner()

    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(build_command, ["--config-file", "tests/mkdocs.yml", "--site-dir", tmpdir])
        assert result.exit_code == 0

        index_file = Path(tmpdir) / "index.html"
        assert index_file.exists(), f"{index_file} does not exist, it should"
        contents = index_file.read_text()

        assert "<pre><code>message Test {" in contents
        assert "<pre><code>message TestMessageA {" in contents
        assert "<pre><code>message TestMessageB {" not in contents
