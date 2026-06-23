"""Unit tests for the file scanner module."""

import pytest
import tempfile
from pathlib import Path
from src.scanner.file_scanner import FileScanner, MediaFile


class TestMediaFile:
    """Tests for MediaFile class."""
    
    def test_media_file_creation(self):
        """Test creating a MediaFile object."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
            media_file = MediaFile(tmp.name)
            assert media_file.name == Path(tmp.name).name
            assert media_file.path == Path(tmp.name)


class TestFileScanner:
    """Tests for FileScanner class."""
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scanner = FileScanner()
            files = scanner.scan(tmpdir)
            assert len(files) == 0
    
    def test_scan_with_media_files(self):
        """Test scanning directory with media files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test media files
            Path(tmpdir, 'photo.jpg').touch()
            Path(tmpdir, 'video.mp4').touch()
            Path(tmpdir, 'document.txt').touch()  # Should be ignored
            
            scanner = FileScanner()
            files = scanner.scan(tmpdir)
            
            assert len(files) == 2
            assert any('photo.jpg' in f.name for f in files)
            assert any('video.mp4' in f.name for f in files)
    
    def test_scan_recursive(self):
        """Test recursive directory scanning."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            subdir = Path(tmpdir) / 'subfolder'
            subdir.mkdir()
            Path(tmpdir, 'photo.jpg').touch()
            Path(subdir, 'video.mp4').touch()
            
            scanner = FileScanner()
            files = scanner.scan(tmpdir)
            
            assert len(files) == 2
