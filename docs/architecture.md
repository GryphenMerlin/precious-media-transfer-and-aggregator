# Architecture Documentation

## Overview

Precious Media Transfer and Aggregator is a Python application that helps users manage, deduplicate, and backup their media files to an external SSD.

## Design Principles

1. **Modularity**: Each component (scanning, deduplication, transfer) is independent
2. **Efficiency**: Hash-based deduplication scales to large media libraries
3. **User-friendly**: Both CLI and GUI interfaces for different use cases
4. **Safety**: Preserves original files; only suggests removals

## Architecture Layers

### 1. Scanner Module (`scanner/`)

**Purpose**: Discover and catalog media files

**Components**:
- `FileScanner`: Recursively scans directories for supported media types
- `MediaFile`: Represents a discovered file with metadata (path, size, hash)
- `MEDIA_EXTENSIONS`: Whitelist of supported file types

**Key Methods**:
- `scan(path)`: Returns list of MediaFile objects found
- `_is_media_file()`: Validates file extension

**Design**: Lazy hashing—files are hashed only when deduplication is needed

---

### 2. Deduplication Module (`deduplication/`)

**Purpose**: Identify and manage duplicate files

**Components**:
- `Deduplicator`: Computes SHA256 hashes and groups duplicates

**Key Methods**:
- `compute_hash(file_path)`: Efficiently computes file hash (chunked reading)
- `find_duplicates(media_files)`: Groups files by hash
- `get_removal_candidates(duplicates)`: Marks oldest file in each group for safe deletion

**Design**: SHA256 chosen for collision resistance and cross-platform compatibility

---

### 3. Transfer Module (`transfer/`)

**Purpose**: Handle file transfers to external SSDs

**Components**:
- `SSDTransfer`: Manages SSD verification and file copying

**Key Methods**:
- `verify_ssd()`: Checks if SSD is accessible and writable
- `create_output_directory()`: Creates destination folder on SSD
- `copy_file()`: Copies individual files
- `transfer_files()`: Bulk transfer with progress tracking
- `get_available_space()`: Checks available disk space
- `get_transfer_size()`: Calculates total data size

**Design**: 
- Validates SSD before transfer
- Prevents overwriting existing files
- Preserves file metadata (timestamps)
- Checks available space before transferring

---

### 4. CLI Interface (`main.py`)

**Purpose**: Command-line interface for automation and scripting

**Commands**:
- `scan`: Discover media files
- `dedupe`: Find duplicates
- `transfer`: Send files to external SSD
- `full-sync`: Complete pipeline in one command

**Design**: Built with Click framework for clean command definition

---

### 5. GUI Interface (`gui.py`)

**Purpose**: Visual interface for non-technical users

**Tabs**:
- **Scan**: Select directories and start scanning
- **Deduplicate**: Review and manage duplicates
- **Transfer to SSD**: Configure SSD path and destination folder

**Design**: PyQt5 with background worker threads to prevent UI blocking

---

## Data Flow

### Typical Usage Flow:

```
User selects source directory
    ↓
FileScanner.scan(path)
    ↓
[MediaFile, MediaFile, ...]
    ↓
Deduplicator.find_duplicates()
    ↓
[[file1, file2], [file3, file4], ...]
    ↓
User reviews duplicates (optional)
    ↓
SSDTransfer.verify_ssd()
    ↓
SSDTransfer.transfer_files()
    ↓
External SSD
```

## Configuration

Configuration is managed by `src/utils/config.py`:
- Environment variables via `.env` file
- Logging levels and output

## SSD Detection & Mounting

### On macOS:
```bash
# List connected SSDs
diskutil list

# SSD mount points typically appear at:
/Volumes/ExternalDrive
/Volumes/SSD_Name
```

### Usage:
```bash
# CLI
python src/main.py transfer --ssd-path /Volumes/MyExternalSSD --output-dir "Media Archive"

# GUI
- Navigate to "Transfer to SSD" tab
- Click "Browse..." to select SSD mount point
- Enter output folder name
- Click "Transfer to SSD"
```

## Future Enhancements

1. **Device Scanning**: Detect connected iPhones/Android devices
2. **Smart Deduplication**: Fuzzy matching for similar images
3. **Background Sync**: Daemon mode for automatic transfers
4. **Database**: Cache hashes to avoid recalculating
5. **Analytics**: Dashboard showing storage savings
6. **Multiple SSDs**: Support simultaneous backup to multiple drives
