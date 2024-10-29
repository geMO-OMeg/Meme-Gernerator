"""
PDF Ingestor Module.

This module contains the PDFIngestor class, which is responsible for
ingesting quotes from PDF files. The class implements the IngestorInterface,
providing methods to check if a PDF file can be ingested and to parse
quotes from the PDF file format.

Classes:
- PDFIngestor: A class for handling the ingestion of PDF files.
  It provides functionality to determine if a file can be ingested based
  on its file extension and to extract quotes from the PDF.

Usage:
To use the PDFIngestor, first check if the file can be ingested using
the `can_ingest` method. If the file can be ingested, call the `parse`
method to extract quotes in the format "quote - author".
"""

from typing import List
import PyPDF2
from .ingestor import IngestorInterface
from .models import QuoteModel

class PDFIngestor(IngestorInterface):
    """
    PDFIngestor is a class for ingesting quotes from PDF files.

    This class implements the IngestorInterface and provides functionality to
    check if a given file can be ingested based on its file extension and to
    parse quotes from the PDF file format.

    Methods:
        can_ingest(path: str) -> bool:
            Determines if the file at the given path can be ingested by checking
            its file extension.

        parse(path: str) -> List[QuoteModel]:
            Parses the specified PDF file and extracts quotes in the format 
            "quote - author". Returns a list of QuoteModel instances.
    """
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Check if the specified file can be ingested.

        Args:
            path (str): The path to the file being checked.

        Returns:
            bool: True if the file is a PDF file, False otherwise.
        """
        return path.endswith('.pdf')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse quotes from a PDF file.

        This method reads the specified PDF file and extracts text from each 
        page. It looks for lines that contain a quote and an author in the 
        format "quote - author". It creates and returns a list of 
        QuoteModel instances representing each parsed quote.

        Args:
            path (str): The path to the PDF file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances containing the 
                              extracted quotes.

        Raises:
            Exception: If an error occurs while opening or reading the file, 
                        the error is logged to an error file.
        """
        quotes = []
        try:
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        for line in text.splitlines():
                            if ' - ' in line:
                                body, author = line.split(' - ')
                                quotes.append(QuoteModel(body=body, author=author))
        except Exception as ex:
            print(f"error with open error, pdf_ingestor line 19: {ex}")
        return quotes