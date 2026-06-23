#!/usr/bin/env python3
"""
GUI entry point for Precious Media Transfer and Aggregator.

Provides a PyQt5-based graphical interface for the application.
"""

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QProgressBar,
    QTextEdit, QTabWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

logger = logging.getLogger(__name__)


class ScanWorker(QThread):
    """Worker thread for scanning files without blocking UI."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)
    
    def __init__(self, source_paths):
        super().__init__()
        self.source_paths = source_paths
    
    def run(self):
        """Execute scan in background."""
        from scanner.file_scanner import FileScanner
        
        scanner = FileScanner()
        all_files = []
        
        for path in self.source_paths:
            self.progress.emit(f"Scanning: {path}")
            files = scanner.scan(path)
            all_files.extend(files)
        
        self.finished.emit(all_files)


class TransferWorker(QThread):
    """Worker thread for transferring files to SSD."""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(tuple)  # (successful, failed, skipped)
    
    def __init__(self, file_list, ssd_path, output_dir):
        super().__init__()
        self.file_list = file_list
        self.ssd_path = ssd_path
        self.output_dir = output_dir
    
    def run(self):
        """Execute transfer in background."""
        from transfer.ssd_transfer import SSDTransfer
        
        transfer = SSDTransfer(self.ssd_path)
        
        if not transfer.verify_ssd():
            self.progress.emit("✗ Error: Could not access SSD")
            self.finished.emit((0, 0, 0))
            return
        
        self.progress.emit("✓ SSD verified")
        
        output = transfer.create_output_directory(self.output_dir)
        if not output:
            self.progress.emit("✗ Error: Could not create output directory")
            self.finished.emit((0, 0, 0))
            return
        
        self.progress.emit(f"✓ Created directory: {output}")
        
        # Calculate transfer size
        total_size = transfer.get_transfer_size(self.file_list)
        self.progress.emit(f"Total size: {total_size / (1024**3):.2f} GB")
        
        # Verify space
        available = transfer.get_available_space()
        if available < total_size:
            self.progress.emit(
                f"✗ Error: Not enough space ({available / (1024**3):.2f} GB available, "
                f"{total_size / (1024**3):.2f} GB needed)"
            )
            self.finished.emit((0, 0, 0))
            return
        
        self.progress.emit("Starting transfer...")
        result = transfer.transfer_files([Path(f.path) for f in self.file_list])
        self.finished.emit(result)


class MediaTransferGUI(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.found_files = []
        self.duplicates = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Precious Media Transfer and Aggregator')
        self.setGeometry(100, 100, 900, 600)
        
        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        
        # Tab widget for different features
        tabs = QTabWidget()
        
        # Tab 1: Scan
        scan_tab = self.create_scan_tab()
        tabs.addTab(scan_tab, "Scan")
        
        # Tab 2: Deduplicate
        dedupe_tab = self.create_dedupe_tab()
        tabs.addTab(dedupe_tab, "Deduplicate")
        
        # Tab 3: Transfer
        transfer_tab = self.create_transfer_tab()
        tabs.addTab(transfer_tab, "Transfer to SSD")
        
        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
    
    def create_scan_tab(self) -> QWidget:
        """Create the scan tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Source path selector
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Source Path:"))
        self.scan_path_input = QLineEdit()
        path_layout.addWidget(self.scan_path_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.select_scan_path)
        path_layout.addWidget(browse_btn)
        
        layout.addLayout(path_layout)
        
        # Scan button
        scan_btn = QPushButton("Start Scan")
        scan_btn.clicked.connect(self.start_scan)
        layout.addWidget(scan_btn)
        
        # Progress bar
        self.scan_progress = QProgressBar()
        layout.addWidget(self.scan_progress)
        
        # Results
        self.scan_output = QTextEdit()
        self.scan_output.setReadOnly(True)
        layout.addWidget(self.scan_output)
        
        tab.setLayout(layout)
        return tab
    
    def create_dedupe_tab(self) -> QWidget:
        """Create the deduplication tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Duplicate Detection"))
        
        dedupe_btn = QPushButton("Find Duplicates")
        dedupe_btn.clicked.connect(self.find_duplicates)
        layout.addWidget(dedupe_btn)
        
        self.dedupe_output = QTextEdit()
        self.dedupe_output.setReadOnly(True)
        layout.addWidget(self.dedupe_output)
        
        tab.setLayout(layout)
        return tab
    
    def create_transfer_tab(self) -> QWidget:
        """Create the SSD transfer tab."""
        tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Transfer to External SSD"))
        
        # SSD path selector
        ssd_layout = QHBoxLayout()
        ssd_layout.addWidget(QLabel("SSD Mount Path:"))
        self.ssd_path_input = QLineEdit()
        ssd_layout.addWidget(self.ssd_path_input)
        
        ssd_browse_btn = QPushButton("Browse...")
        ssd_browse_btn.clicked.connect(self.select_ssd_path)
        ssd_layout.addWidget(ssd_browse_btn)
        
        layout.addLayout(ssd_layout)
        
        # Output folder name
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Output Folder:"))
        self.transfer_folder_input = QLineEdit("Media Archive")
        folder_layout.addWidget(self.transfer_folder_input)
        layout.addLayout(folder_layout)
        
        # Transfer button
        transfer_btn = QPushButton("Transfer to SSD")
        transfer_btn.clicked.connect(self.start_transfer)
        layout.addWidget(transfer_btn)
        
        # Progress bar
        self.transfer_progress = QProgressBar()
        layout.addWidget(self.transfer_progress)
        
        # Output
        self.transfer_output = QTextEdit()
        self.transfer_output.setReadOnly(True)
        layout.addWidget(self.transfer_output)
        
        tab.setLayout(layout)
        return tab
    
    def select_scan_path(self):
        """Open file dialog to select scan path."""
        path = QFileDialog.getExistingDirectory(self, "Select Directory to Scan")
        if path:
            self.scan_path_input.setText(path)
    
    def select_ssd_path(self):
        """Open file dialog to select SSD path."""
        path = QFileDialog.getExistingDirectory(self, "Select SSD Mount Point")
        if path:
            self.ssd_path_input.setText(path)
    
    def start_scan(self):
        """Start scanning for media files."""
        path = self.scan_path_input.text()
        if not path:
            QMessageBox.warning(self, "Error", "Please select a path to scan")
            return
        
        self.scan_output.setText("Scanning...\n")
        self.worker = ScanWorker([path])
        self.worker.progress.connect(self.update_scan_output)
        self.worker.finished.connect(self.scan_complete)
        self.worker.start()
    
    def update_scan_output(self, message: str):
        """Update scan output with progress."""
        self.scan_output.append(message)
    
    def scan_complete(self, files: list):
        """Handle scan completion."""
        self.found_files = files
        self.scan_output.append(f"\n✓ Scan complete: {len(files)} files found")
    
    def find_duplicates(self):
        """Find duplicate files."""
        if not self.found_files:
            QMessageBox.warning(self, "Error", "Please scan files first")
            return
        
        from deduplication.deduplicator import Deduplicator
        
        deduplicator = Deduplicator()
        self.duplicates = deduplicator.find_duplicates(self.found_files)
        
        output = f"Found {len(self.duplicates)} duplicate groups:\n"
        for i, group in enumerate(self.duplicates, 1):
            output += f"\nGroup {i}: {len(group)} files\n"
            for file in group:
                output += f"  - {file.name}\n"
        
        self.dedupe_output.setText(output)
    
    def start_transfer(self):
        """Start transferring files to SSD."""
        ssd_path = self.ssd_path_input.text()
        output_dir = self.transfer_folder_input.text()
        
        if not ssd_path:
            QMessageBox.warning(self, "Error", "Please select an SSD path")
            return
        
        if not output_dir:
            QMessageBox.warning(self, "Error", "Please enter an output folder name")
            return
        
        if not self.found_files:
            QMessageBox.warning(self, "Error", "Please scan files first")
            return
        
        self.transfer_output.setText("Starting transfer...\n")
        self.transfer_worker = TransferWorker(self.found_files, ssd_path, output_dir)
        self.transfer_worker.progress.connect(self.update_transfer_output)
        self.transfer_worker.finished.connect(self.transfer_complete)
        self.transfer_worker.start()
    
    def update_transfer_output(self, message: str):
        """Update transfer output with progress."""
        self.transfer_output.append(message)
    
    def transfer_complete(self, result: tuple):
        """Handle transfer completion."""
        successful, failed, skipped = result
        self.transfer_output.append(
            f"\n✓ Transfer complete!\n"
            f"  Successful: {successful}\n"
            f"  Failed: {failed}\n"
            f"  Skipped: {skipped}"
        )


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    window = MediaTransferGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
