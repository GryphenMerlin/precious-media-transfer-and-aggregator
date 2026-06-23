# Architecture Documentation

## Overview

Precious Media Transfer and Aggregator is a Python application that helps users manage, deduplicate, and backup their media files to Google Drive.

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

**Purpose**: Handle Google Drive authentication and uploads

**Components**:
- `DriveUploader`: Manages OAuth 2.0 flow and file uploads

**Key Methods**:
- `authenticate()`: OAuth 2.0 flow with Google
- `create_folder()`: Creates destination folder on Drive
- `upload_file()`: Uploads individual files

**Design**: Async uploads planned for future version

---

### 4. CLI Interface (`main.py`)

**Purpose**: Command-line interface for automation and scripting

**Commands**:
- `scan`: Discover media files
- `dedupe`: Find duplicates
- `upload`: Send files to Google Drive
- `full-sync`: Complete pipeline in one command

**Design**: Built with Click framework for clean command definition

---

### 5. GUI Interface (`gui.py`)

**Purpose**: Visual interface for non-technical users

**Tabs**:
- **Scan**: Select directories and start scanning
- **Deduplicate**: Review and manage duplicates
- **Upload**: Configure Google Drive destination

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
User reviews duplicates (decide which to remove)
    ↓
DriveUploader.upload_file()
    ↓
Google Drive
```

## Configuration

Configuration is managed by `src/utils/config.py`:
- Environment variables via `.env` file
- Google OAuth credentials path
- Logging levels and output

## Future Enhancements

1. **Device Scanning**: Detect connected iPhones/Android devices
2. **Smart Deduplication**: Fuzzy matching for similar images
3. **Background Sync**: Daemon mode for automatic uploads
4. **Database**: Cache hashes to avoid recalculating
5. **Analytics**: Dashboard showing storage savings
