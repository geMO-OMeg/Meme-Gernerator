"""
TXT Ingestor Module.

This module contains the TXTIngestor class, which is responsible for
ingesting quotes from plain text (.txt) files. The class implements
the IngestorInterface, providing methods to determine if a TXT file
can be ingested and to parse quotes from the TXT file format.

Classes:
- TXTIngestor: A class for handling the ingestion of TXT files.
  It provides functionality to check if a file can be ingested based
  on its file extension and to extract quotes in the format "quote - author".

Usage:
To use the TXTIngestor, first check if the file can be ingested using
the `can_ingest` method. If the file can be ingested, call the `parse`
method to extract quotes.
"""

from typing import List
from .ingestor import IngestorInterface
from .models import QuoteModel

class TXTIngestor(IngestorInterface):
    """
    TXTIngestor is a class for ingesting quotes from TXT files.

    This class implements the IngestorInterface and provides functionality to
    check if a given file can be ingested based on its file extension and to
    parse quotes from the TXT file format.

    Methods:
        can_ingest(path: str) -> bool:
            Determines if the file at the given path can be ingested by checking
            its file extension.

        parse(path: str) -> List[QuoteModel]:
            Parses the specified TXT file and extracts quotes in the format 
            "quote - author". Returns a list of QuoteModel instances.
    """
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Check if the specified file can be ingested.

        Args:
            path (str): The path to the file being checked.

        Returns:
            bool: True if the file is a TXT file, False otherwise.
        """
        return path.endswith('.txt')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse quotes from a TXT file.

        This method reads the specified TXT file line by line, looking for lines 
        that contain a quote and an author in the format "quote - author".
        It creates and returns a list of QuoteModel instances representing each 
        parsed quote.

        Args:
            path (str): The path to the TXT file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances containing the 
                              extracted quotes.

        Raises:
            Exception: If an error occurs while opening or reading the file, 
                        the error is logged to an error file.
        """
        quotes = []
        try:
            with open(path, 'r', encoding='utf-8-sig') as file:
                for line in file:
                    if ' - ' in line:
                        body, author = line.split(' - ')
                        quotes.append(QuoteModel(body=body.strip(), author=author.strip()))
        except Exception as ex:
            print(f"error with open error, txt_ingestor: {ex}")
        return quotes
