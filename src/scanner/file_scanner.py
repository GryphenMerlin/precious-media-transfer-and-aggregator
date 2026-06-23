"""Scans directories for media files (photos and videos)."""

import os
from pathlib import Path
from typing import List, Set
import logging

logger = logging.getLogger(__name__)

# Supported media file extensions
MEDIA_EXTENSIONS: Set[str] = {
    # Photos
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.raw', '.heic', '.heif',
    # Videos
    '.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.m4v', '.3gp', '.ts'
}


class MediaFile:
    """Represents a discovered media file."""
    
    def __init__(self, path: str):
        self.path = Path(path)
        self.name = self.path.name
        self.size = self.path.stat().st_size
        self.hash = None  # Will be computed on demand
    
    def __repr__(self):
        return f"MediaFile({self.name}, {self.size} bytes)"


class FileScanner:
    """Scans directories recursively for media files."""
    
    def __init__(self):
        self.found_files: List[MediaFile] = []
    
    def scan(self, source_path: str) -> List[MediaFile]:
        """Recursively scan a directory for media files.
        
        Args:
            source_path: Directory path to scan
            
        Returns:
            List of MediaFile objects found
        """
        self.found_files = []
        root = Path(source_path)
        
        if not root.exists():
            logger.error(f"Path does not exist: {source_path}")
            return []
        
        if not root.is_dir():
            logger.warning(f"Path is not a directory: {source_path}")
            return []
        
        for file_path in root.rglob('*'):
            if file_path.is_file():
                if self._is_media_file(file_path):
                    self.found_files.append(MediaFile(str(file_path)))
                    logger.debug(f"Found: {file_path}")
        
        logger.info(f"Scan complete: {len(self.found_files)} files in {source_path}")
        return self.found_files
    
    @staticmethod
    def _is_media_file(file_path: Path) -> bool:
        """Check if file is a supported media type."""
        return file_path.suffix.lower() in MEDIA_EXTENSIONS
