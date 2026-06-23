"""Configuration management."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / '.data'
    
    # Google Drive
    GOOGLE_CREDENTIALS_FILE = os.getenv(
        'GOOGLE_CREDENTIALS_FILE',
        str(BASE_DIR / 'credentials.json')
    )
    GOOGLE_TOKEN_FILE = os.getenv(
        'GOOGLE_TOKEN_FILE',
        str(BASE_DIR / 'token.pickle')
    )
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = DATA_DIR / 'app.log'
    
    @classmethod
    def ensure_dirs(cls):
        """Create necessary directories."""
        cls.DATA_DIR.mkdir(exist_ok=True)


if __name__ == '__main__':
    Config.ensure_dirs()
    print(f"Base directory: {Config.BASE_DIR}")
    print(f"Data directory: {Config.DATA_DIR}")
