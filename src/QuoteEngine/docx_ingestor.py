"""
DOCX Ingestor Module.

This module contains the DOCXIngestor class, which is responsible for
ingesting quotes from .docx files. The class implements the IngestorInterface,
providing methods to determine if a file can be ingested and to parse
the contents of the file into QuoteModel instances.

Classes:
- DOCXIngestor: A class for handling the ingestion of .docx files.
  It provides functionality to check if a .docx file can be ingested
  and to parse the file to extract quotes.

Usage:
To use the DOCXIngestor, check if a .docx file can be ingested using
the `can_ingest` method. If the file can be ingested, call the `parse`
method to extract quotes in the format "quote - author".
"""

from typing import List
from docx import Document
from .ingestor import IngestorInterface
from .models import QuoteModel

class DOCXIngestor(IngestorInterface):
    """
    Ingestor class for handling the ingestion of .docx files.

    This class implements the IngestorInterface, providing functionality
    to check if a .docx file can be ingested and to parse the file
    to extract quotes.

    Methods:
        can_ingest(cls, path: str) -> bool:
            Checks if the specified file can be ingested.
        
        parse(cls, path: str) -> List[QuoteModel]:
            Parses the .docx file and returns a list of QuoteModel instances.
    """
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the ingestor can handle the specified .docx file.

        Args:
            cls: The class itself.
            path (str): The path to the file to check.

        Returns:
            bool: True if the file can be ingested (i.e., it ends with .docx), False otherwise.
        """
        return path.endswith('.docx')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse the specified .docx file to extract quotes.

        The method reads the document, splits each paragraph by the 
        delimiter ' - ', and creates QuoteModel instances from the 
        resulting body and author.

        Args:
            cls: The class itself.
            path (str): The path to the .docx file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances extracted from the file.

        Raises:
            Exception: Any exceptions raised during file reading are logged to an error file.
        """
        quotes = []
        try:
            doc = Document(path)
            for para in doc.paragraphs:
                if para.text:
                    body, author = para.text.split(' - ')  # Assuming format "quote - author"
                    quotes.append(QuoteModel(body=body, author=author))
        except Exception as ex:
            print(f"error with open error, docx_ingestor line 19: {ex}")
        return quotes