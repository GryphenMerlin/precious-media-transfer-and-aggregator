# Precious Media Transfer and Aggregator

An app that scans your Mac and connected devices for media (photos and videos), transfers them to Google Drive, and checks for duplicates.

## Features

- 🔍 **Smart Scanning**: Recursively scans Mac and connected devices for photos and videos
- 📤 **Google Drive Integration**: Automatically uploads media to Google Drive
- 🔐 **Duplicate Detection**: Uses file hashing to identify and eliminate duplicates
- ⚡ **Efficient Transfers**: Only uploads new/non-duplicate files
- 🖥️ **Dual Interface**: CLI for automation, GUI for ease of use

## Quick Start

### Prerequisites
- Python 3.9+
- macOS
- Google Drive account (for storage)

### Installation

```bash
git clone https://github.com/GryphenMerlin/precious-media-transfer-and-aggregator.git
cd precious-media-transfer-and-aggregator
pip install -r requirements.txt
```

### CLI Usage

```bash
# Scan local media
python src/main.py scan ~/Pictures ~/Movies

# Upload to Google Drive
python src/main.py upload --output-dir "Media Archive"

# Check for duplicates
python src/main.py dedupe --source ~/Pictures

# Full pipeline: scan, dedupe, upload
python src/main.py full-sync ~/Pictures --output-dir "Media Archive"
```

### GUI Usage

```bash
python src/gui.py
```

## Project Structure

```
src/
├── main.py              # CLI entry point
├── gui.py               # GUI entry point (PyQt5)
├── scanner/             # File discovery and metadata extraction
├── deduplication/       # Duplicate detection via hashing
├── transfer/            # Google Drive API integration
└── utils/               # Helpers (logging, config, etc.)

tests/                   # Unit and integration tests
docs/                    # Architecture and design docs
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed design documentation.

## Contributing

Contributions welcome! Please read our contributing guidelines.

## License

MIT
