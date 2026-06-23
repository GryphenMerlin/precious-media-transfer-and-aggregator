"""SSD file transfer management for external drives."""

import logging
import shutil
from pathlib import Path
from typing import Optional, List
import os

logger = logging.getLogger(__name__)


class SSDTransfer:
    """Handles file transfers to external SSDs."""
    
    def __init__(self, ssd_path: str):
        """Initialize SSD transfer manager.
        
        Args:
            ssd_path: Path to the external SSD mount point
        """
        self.ssd_path = Path(ssd_path)
        self.output_dir = None
    
    def verify_ssd(self) -> bool:
        """Verify that the SSD is accessible and writable.
        
        Returns:
            True if SSD is accessible, False otherwise
        """
        try:
            if not self.ssd_path.exists():
                logger.error(f"SSD path does not exist: {self.ssd_path}")
                return False
            
            if not os.access(self.ssd_path, os.W_OK):
                logger.error(f"No write permission on SSD: {self.ssd_path}")
                return False
            
            logger.info(f"SSD verified: {self.ssd_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify SSD: {e}")
            return False
    
    def create_output_directory(self, dir_name: str) -> Optional[Path]:
        """Create output directory on SSD.
        
        Args:
            dir_name: Name of the output directory
            
        Returns:
            Path to created directory, or None if failed
        """
        try:
            output_path = self.ssd_path / dir_name
            output_path.mkdir(parents=True, exist_ok=True)
            self.output_dir = output_path
            logger.info(f"Created output directory: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to create output directory: {e}")
            return None
    
    def get_available_space(self) -> int:
        """Get available space on SSD in bytes.
        
        Returns:
            Available space in bytes
        """
        try:
            stat = os.statvfs(self.ssd_path)
            available = stat.f_bavail * stat.f_frsize
            logger.info(f"Available space on SSD: {available / (1024**3):.2f} GB")
            return available
        except Exception as e:
            logger.error(f"Failed to get available space: {e}")
            return 0
    
    def copy_file(self, source_path: Path, preserve_structure: bool = True) -> Optional[Path]:
        """Copy a file to the SSD output directory.
        
        Args:
            source_path: Path to source file
            preserve_structure: If True, preserve subdirectory structure
            
        Returns:
            Path to copied file, or None if failed
        """
        if not self.output_dir:
            logger.error("Output directory not set. Call create_output_directory() first.")
            return None
        
        try:
            source = Path(source_path)
            
            if preserve_structure:
                # Preserve relative directory structure
                dest = self.output_dir / source.name
            else:
                dest = self.output_dir / source.name
            
            # Avoid overwriting existing files
            if dest.exists():
                logger.warning(f"File already exists on SSD, skipping: {dest}")
                return dest
            
            # Copy file
            shutil.copy2(source, dest)
            logger.info(f"Copied: {source.name} -> {dest}")
            return dest
        except Exception as e:
            logger.error(f"Failed to copy file {source_path}: {e}")
            return None
    
    def transfer_files(self, file_list: List[Path], skip_duplicates: bool = True) -> tuple:
        """Transfer multiple files to SSD.
        
        Args:
            file_list: List of file paths to transfer
            skip_duplicates: Skip files that already exist on SSD
            
        Returns:
            Tuple of (successful_count, failed_count, skipped_count)
        """
        if not self.output_dir:
            logger.error("Output directory not set.")
            return (0, 0, 0)
        
        successful = 0
        failed = 0
        skipped = 0
        
        logger.info(f"Starting transfer of {len(file_list)} files...")
        
        for file_path in file_list:
            dest = self.copy_file(file_path)
            
            if dest is None:
                failed += 1
            elif dest.exists() and skip_duplicates:
                skipped += 1
            else:
                successful += 1
        
        logger.info(
            f"Transfer complete: {successful} successful, {failed} failed, {skipped} skipped"
        )
        return (successful, failed, skipped)
    
    def get_transfer_size(self, file_list: List[Path]) -> int:
        """Calculate total size of files to transfer.
        
        Args:
            file_list: List of file paths
            
        Returns:
            Total size in bytes
        """
        total_size = 0
        for file_path in file_list:
            try:
                total_size += Path(file_path).stat().st_size
            except OSError:
                pass
        return total_size
