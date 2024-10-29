"""
CSVIngestor Module.

This module defines the CSVIngestor class, which is responsible for ingesting 
quotes from CSV files. It inherits from the IngestorInterface and provides 
methods for determining if a file can be ingested and for parsing the 
file into a list of QuoteModel instances.

Classes:
- CSVIngestor: A class for reading quotes from CSV files and converting 
  them into QuoteModel instances.

Usage:
To use the CSVIngestor, call the `can_ingest` method to check if a given 
file is a CSV file, and then use the `parse` method to read the file 
and extract quotes.
"""

import csv
from typing import List
from .ingestor import IngestorInterface
from .models import QuoteModel


class CSVIngestor(IngestorInterface):
    """
    CSVIngestor is a class for ingesting quotes from CSV files.

    Inherits from IngestorInterface and implements methods to determine
    if a file can be ingested and to parse the file into a list of
    QuoteModel instances.

    Attributes:
        error_file (str): Path to the error log file where errors will be recorded.
    """
     
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determine if the specified file can be ingested.

        Checks if the provided file path ends with the '.csv' extension.

        Args:
            path (str): The file path to check.

        Returns:
            bool: True if the file can be ingested, False otherwise.
        """
        return path.endswith('.csv')

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Parse a CSV file and return a list of QuoteModel instances.

        Reads a CSV file from the specified path, skipping the header row,
        and creates QuoteModel instances for each quote-author pair found
        in the file.

        Args:
            path (str): The path to the CSV file to be parsed.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances containing
            the quotes and their respective authors.

        Logs any exceptions that occur during file processing to the
        error log file specified by error_file.
        """
        quotes = []
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if len(row) == 2:
                        quotes.append(QuoteModel(body=row[0], author=row[1]))
        except Exception as ex:
            print(f"error with open error, csv_ingestor line 19: {ex}")
        return quotes
