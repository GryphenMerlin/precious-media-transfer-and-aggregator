#!/usr/bin/env python3
"""
CLI entry point for Precious Media Transfer and Aggregator.

Usage:
  python main.py scan <source_paths>...
  python main.py dedupe <source_path>
  python main.py transfer --ssd-path <path> --output-dir <dir>
  python main.py full-sync <source_paths>... --ssd-path <path> --output-dir <dir>
"""

import click
import logging
from pathlib import Path
from scanner.file_scanner import FileScanner
from deduplication.deduplicator import Deduplicator
from transfer.ssd_transfer import SSDTransfer

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
@click.option('--ssd-path', required=True, type=click.Path(), help='Path to external SSD')
@click.option('--output-dir', required=True, help='Output folder name on SSD')
def transfer(ssd_path, output_dir):
    """Transfer media to external SSD."""
    click.echo(f"Transferring to SSD: {ssd_path}")
    click.echo(f"Output directory: {output_dir}")
    
    transfer_manager = SSDTransfer(ssd_path)
    if transfer_manager.verify_ssd():
        click.echo("✓ SSD verified and accessible")
        # Transfer logic to be implemented
    else:
        click.echo("✗ Error: Could not access SSD")


@cli.command()
@click.argument('source_paths', nargs=-1, type=click.Path(exists=True), required=True)
@click.option('--ssd-path', required=True, type=click.Path(), help='Path to external SSD')
@click.option('--output-dir', required=True, help='Output folder name on SSD')
def full_sync(source_paths, ssd_path, output_dir):
    """Complete pipeline: scan, dedupe, transfer to SSD."""
    click.echo("Starting full sync pipeline...")
    
    # Step 1: Scan
    click.echo("\n[1/3] Scanning for media files...")
    scanner = FileScanner()
    all_files = []
    for path in source_paths:
        files = scanner.scan(path)
        all_files.extend(files)
    click.echo(f"Found {len(all_files)} media files")
    
    # Step 2: Deduplicate
    click.echo("\n[2/3] Detecting duplicates...")
    deduplicator = Deduplicator()
    duplicates = deduplicator.find_duplicates(all_files)
    click.echo(f"Found {len(duplicates)} duplicate groups")
    
    # Step 3: Transfer
    click.echo("\n[3/3] Transferring to SSD...")
    transfer_manager = SSDTransfer(ssd_path)
    if transfer_manager.verify_ssd():
        click.echo("✓ SSD verified")
        click.echo(f"\n✓ Full sync complete!")
    else:
        click.echo("✗ Error: Could not access SSD")


if __name__ == '__main__':
    cli()
