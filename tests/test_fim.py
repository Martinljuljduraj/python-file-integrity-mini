import pytest
import tempfile
import os
from pathlib import Path
from fim import hash_file, scan_directory, compare

def test_same_file_hashes_twice():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(b"hello world")
        tmp_path = Path(tmp.name)
    try:
        result1 = hash_file(tmp_path)
        result2 = hash_file(tmp_path)
        assert result1 == result2
    finally:
        os.unlink(tmp_path)

def test_changing_content_changes_hash():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        tmp.write(b"original content")
        tmp_path = Path(tmp.name)
    try:
        hash1 = hash_file(tmp_path)
        tmp_path.write_text("modified content")
        hash2 = hash_file(tmp_path)
        assert hash1 != hash2
    finally:
        os.unlink(tmp_path)

def test_new_files_detected():
    baseline = {
        "files": {
            "file1.txt": {"sha256": "abc123"}
        }
    }
    current = {
        "file1.txt": {"sha256": "abc123"},
        "file2.txt": {"sha256": "def456"}
    }
    changes = compare(baseline, current)
    assert "file2.txt" in changes["new"]

def test_deleted_files_detected():
    baseline = {
        "files": {
            "file1.txt": {"sha256": "abc123"},
            "file2.txt": {"sha256": "def456"}
        }
    }
    current = {
        "file1.txt": {"sha256": "abc123"}
    }
    changes = compare(baseline, current)
    assert "file2.txt" in changes["deleted"]

def test_modified_files_detected():
    baseline = {
        "files": {
            "file1.txt": {"sha256": "abc123"}
        }
    }
    current = {
        "file1.txt": {"sha256": "xyz999"}
    }
    changes = compare(baseline, current)
    assert "file1.txt" in changes["modified"]

def test_ignored_directories_skipped():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "venv").mkdir()
        (root / "venv" / "file.txt").write_text("should be ignored")
        (root / "normal.txt").write_text("should be scanned")
        results = scan_directory(root)
        assert "venv/file.txt" not in results
        assert "normal.txt" in results