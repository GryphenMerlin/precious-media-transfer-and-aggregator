"""Detects duplicate files using content hashing."""

import hashlib
from typing import Dict, List, Set
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class Deduplicator:
    """Identifies duplicate files by computing file hashes."""
    
    HASH_ALGORITHM = 'sha256'
    CHUNK_SIZE = 8192  # Read file in 8KB chunks
    
    def __init__(self):
        self.hash_map: Dict[str, List] = defaultdict(list)
    
    def compute_hash(self, file_path: str) -> str:
        """Compute SHA256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hex digest of the file's hash
        """
        hasher = hashlib.sha256()
        
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(self.CHUNK_SIZE):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except IOError as e:
            logger.error(f"Failed to hash {file_path}: {e}")
            return None
    
    def find_duplicates(self, media_files: List) -> List[List]:
        """Find all duplicate file groups.
        
        Args:
            media_files: List of MediaFile objects
            
        Returns:
            List of duplicate groups (each group has 2+ identical files)
        """
        self.hash_map.clear()
        
        # Build hash map
        for media_file in media_files:
            file_hash = self.compute_hash(str(media_file.path))
            if file_hash:
                self.hash_map[file_hash].append(media_file)
        
        # Extract duplicates (hash appears 2+ times)
        duplicates = [
            group for group in self.hash_map.values()
            if len(group) > 1
        ]
        
        logger.info(f"Found {len(duplicates)} duplicate groups")
        return duplicates
    
    def get_removal_candidates(self, duplicates: List[List]) -> List:
        """Get list of files to remove (keeps oldest file in each group).
        
        Args:
            duplicates: List of duplicate groups
            
        Returns:
            List of files recommended for deletion
        """
        candidates = []
        
        for group in duplicates:
            # Sort by modification time, keep the oldest
            sorted_group = sorted(
                group,
                key=lambda f: f.path.stat().st_mtime
            )
            # Add all but the oldest to removal list
            candidates.extend(sorted_group[1:])
        
        logger.info(f"Identified {len(candidates)} files for potential removal")
        return candidates
