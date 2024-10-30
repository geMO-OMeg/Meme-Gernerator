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
import subprocess
import os
from .ingestor import IngestorInterface
from .models import QuoteModel

error_file = './_data/errorFile.txt'

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

        This method invokes the pdftotext CLI utility to convert the PDF file to
        text. It then processes the extracted text to find quotes and their
        authors in the format "quote - author". A list of QuoteModel instances
        representing each parsed quote is returned.

        Args:
            path (str): The path to the PDF file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances containing the 
                              extracted quotes.

        Raises:
            Exception: If an error occurs while invoking pdftotext or processing
                        the extracted text.
        """
        quotes = []
        tmp = './_data/SimpleLines/temp.txt'

        try:
            # Invoke the pdftotext CLI utility
            subprocess.call(['pdftotext', path, tmp])

            # Read the extracted text
            with open(tmp, 'r', encoding='utf-8') as file:
                for line in file:
                    if ' - ' in line:
                        body, author = line.split(' - ')
                        quotes.append(QuoteModel(body=body.strip(), author=author.strip()))
                        if os.path.exists(tmp):
                            os.remove(tmp)
        except Exception as ex:
            print(f"Error while processing PDF: {ex}")
            with open(error_file, 'a') as f:
                f.write(f"\nerror with open, pdf_ingestor.py: {ex}")
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp):
                os.remove(tmp)

        return quotes