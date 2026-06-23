"""Unit tests for the deduplication module."""

import pytest
import tempfile
from pathlib import Path
from src.deduplication.deduplicator import Deduplicator
from src.scanner.file_scanner import MediaFile


class TestDeduplicator:
    """Tests for Deduplicator class."""
    
    def test_compute_hash(self):
        """Test file hash computation."""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b'test content')
            tmp.flush()
            
            deduplicator = Deduplicator()
            hash1 = deduplicator.compute_hash(tmp.name)
            hash2 = deduplicator.compute_hash(tmp.name)
            
            assert hash1 == hash2
            assert len(hash1) == 64  # SHA256 hex digest is 64 chars
    
    def test_find_duplicates(self):
        """Test finding duplicate files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create identical files
            file1 = Path(tmpdir) / 'file1.jpg'
            file2 = Path(tmpdir) / 'file2.jpg'
            file3 = Path(tmpdir) / 'file3.jpg'
            
            # Write same content to file1 and file2
            file1.write_bytes(b'identical content')
            file2.write_bytes(b'identical content')
            file3.write_bytes(b'different content')
            
            media_files = [
                MediaFile(str(file1)),
                MediaFile(str(file2)),
                MediaFile(str(file3))
            ]
            
            deduplicator = Deduplicator()
            duplicates = deduplicator.find_duplicates(media_files)
            
            assert len(duplicates) == 1
            assert len(duplicates[0]) == 2
