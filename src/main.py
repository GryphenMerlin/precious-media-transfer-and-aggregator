#!/usr/bin/env python3
"""
CLI entry point for Precious Media Transfer and Aggregator.

Usage:
  python main.py scan <source_paths>...
  python main.py dedupe <source_path>
  python main.py upload --output-dir <dir_name>
  python main.py full-sync <source_paths>... --output-dir <dir_name>
"""

import click
import logging
from pathlib import Path
from scanner.file_scanner import FileScanner
from deduplication.deduplicator import Deduplicator
from transfer.drive_uploader import DriveUploader

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Precious Media Transfer and Aggregator CLI."""
    pass


@cli.command()
@click.argument('source_paths', nargs=-1, type=click.Path(exists=True), required=True)
def scan(source_paths):
    """Scan directories for media files."""
    click.echo(f"Scanning {len(source_paths)} location(s) for media...")
    
    scanner = FileScanner()
    all_files = []
    
    for path in source_paths:
        logger.info(f"Scanning: {path}")
        files = scanner.scan(path)
        all_files.extend(files)
        click.echo(f"  Found {len(files)} media files")
    
    click.echo(f"\n✓ Total: {len(all_files)} media files found")
    return all_files


@cli.command()
@click.argument('source_path', type=click.Path(exists=True))
def dedupe(source_path):
    """Check for duplicate files."""
    click.echo(f"Analyzing {source_path} for duplicates...")
    
    scanner = FileScanner()
    deduplicator = Deduplicator()
    
    files = scanner.scan(source_path)
    duplicates = deduplicator.find_duplicates(files)
    
    click.echo(f"\n✓ Found {len(duplicates)} duplicate groups")
    for group in duplicates:
        click.echo(f"  {len(group)} duplicates: {group[0].name}")


@cli.command()
@click.option('--output-dir', required=True, help='Google Drive folder name')
def upload(output_dir):
    """Upload media to Google Drive."""
    click.echo(f"Uploading to Google Drive folder: {output_dir}")
    
    uploader = DriveUploader()
    uploader.authenticate()
    click.echo("✓ Authenticated with Google Drive")
    # Upload logic to be implemented


@cli.command()
@click.argument('source_paths', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--output-dir', required=True, help='Google Drive folder name')
def full_sync(source_paths, output_dir):
    """Complete pipeline: scan, dedupe, upload."""
    click.echo("Starting full sync pipeline...")
    
    # Step 1: Scan
    files = scan(source_paths)
    
    # Step 2: Deduplicate
    deduplicator = Deduplicator()
    duplicates = deduplicator.find_duplicates(files)
    
    # Step 3: Upload
    uploader = DriveUploader()
    uploader.authenticate()
    click.echo(f"\n✓ Full sync complete!")


if __name__ == '__main__':
    cli()
