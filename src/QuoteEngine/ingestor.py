# QuoteEngine/ingestor.py

from abc import ABC, abstractmethod
from typing import List
from .models import QuoteModel

class IngestorInterface(ABC):
    """
    Abstract base class for defining the interface for ingestor classes.

    This class establishes the contract that all ingestor implementations
    must follow. It defines the abstract methods for checking if a file
    can be ingested and for parsing the file to extract quotes.

    Methods:
        can_ingest(cls, path: str) -> bool:
            Determines if the ingestor can process the given file path.
        
        parse(cls, path: str) -> List[QuoteModel]:
            Parses the given file and returns a list of QuoteModel instances.
    """

    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Abstract method to determine if the ingestor can handle the specified file.

        Args:
            cls: The class itself.
            path (str): The path to the file to check.

        Returns:
            bool: True if the file can be ingested, False otherwise.
        """
        pass

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """
        Abstract method to parse the specified file and extract quotes.

        Args:
            cls: The class itself.
            path (str): The path to the file to parse.

        Returns:
            List[QuoteModel]: A list of QuoteModel instances extracted from the file.
        """
        pass



class Ingestor:
    """
    Ingestor class that utilizes various ingestor implementations
    to determine the correct one for handling a specific file type.

    This class provides a method to parse files by delegating to the
    appropriate ingestor based on the file type.

    Methods:
        parse(cls, path: str) -> List:
            Parses the given file path using the appropriate ingestor.
    """

    @classmethod
    def parse(cls, path: str) -> List:
        """
        Parses the specified file using the appropriate ingestor.

        This method checks the file path against known ingestor classes
        and uses the first one that can handle the file type.

        Args:
            cls: The class itself.
            path (str): The path to the file to be parsed.

        Returns:
            List: A list of quotes extracted from the file.

        Raises:
            Exception: If no ingestor can handle the specified file type.
        """
        from .csv_ingestor import CSVIngestor
        from .docx_ingestor import DOCXIngestor
        from .pdf_ingestor import PDFIngestor
        from .txt_ingestor import TXTIngestor
        
        ingestors = [CSVIngestor, DOCXIngestor, PDFIngestor, TXTIngestor]
        
        for ingestor in ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise Exception(f'Cannot ingest file at {path}')
    