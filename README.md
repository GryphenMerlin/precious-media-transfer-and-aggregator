# Precious Media Transfer and Aggregator

An app that scans your Mac and connected devices for media (photos and videos), transfers them to an attached SSD, and checks for duplicates.

## Features

- 🔍 **Smart Scanning**: Recursively scans Mac and connected devices for photos and videos
- 💾 **SSD Transfer**: Automatically copies media to an attached external SSD
- 🔍 **Duplicate Detection**: Uses file hashing to identify and eliminate duplicates
- ⚡ **Efficient Transfers**: Only copies new/non-duplicate files
- 🖥️ **Dual Interface**: CLI for automation, GUI for ease of use

## Quick Start

### Prerequisites
- Python 3.9+
- macOS
- External SSD (for storage)

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

# Transfer to SSD
python src/main.py transfer --ssd-path /Volumes/MyExternalSSD --output-dir "Media Archive"

# Check for duplicates
python src/main.py dedupe ~/Pictures

# Full pipeline: scan, dedupe, transfer to SSD
python src/main.py full-sync ~/Pictures --ssd-path /Volumes/MyExternalSSD --output-dir "Media Archive"
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
├── transfer/            # SSD file transfer logic
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
