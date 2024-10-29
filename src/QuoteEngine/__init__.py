"""
QuoteEngine Package.

This package provides functionality for handling quotes, including ingesting
quotes from various file formats and defining quote models.

Modules:
- Ingestor: Responsible for parsing different quote file formats.
- QuoteModel: Defines the structure for quote objects.
"""

from .ingestor import Ingestor
from .models import QuoteModel