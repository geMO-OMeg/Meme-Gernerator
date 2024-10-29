"""
QuoteModel Module.

This module defines the QuoteModel class, which represents a quote along 
with its associated author. The QuoteModel encapsulates the quote text and 
author information, providing functionality to clean and format the quote 
for easy display.

Classes:
- QuoteModel: A class for creating and managing quotes, including methods 
  for cleaning text and generating a string representation of the quote.

Usage:
To create a quote, instantiate the QuoteModel class with the quote text and 
author. Use the `__str__()` method to obtain a formatted representation of 
the quote.

Example:
    quote = QuoteModel("To be, or not to be.", "William Shakespeare")
    print(quote)  # Output: "To be, or not to be." - William Shakespeare
"""

class QuoteModel:
    """
    Represents a quote with its associated author.

    The QuoteModel class is used to encapsulate a quote along with its author.
    It provides methods to clean the quote text and format it as a string for 
    easy display.

    Attributes:
        body (str): The text of the quote.
        author (str): The author of the quote.

    Methods:
        __str__() -> str:
            Returns a formatted string representation of the quote.
        
        clean_text(text: str) -> str:
            Cleans the provided text by replacing specific unicode characters 
            with their ASCII equivalents.
    """
    
    def __init__(self, body: str, author: str):
        """
        Initialize a QuoteModel instance with the provided quote body and author.

        Args:
            body (str): The text of the quote.
            author (str): The author of the quote.
        """
        self.body = self.clean_text(body.strip())
        self.author = self.clean_text(author.strip())

    def __str__(self):
        """
        Return a string representation of the quote in the format: "quote" - author.

        Returns:
            str: A formatted string representing the quote and its author.
        """
        return f'"{self.body}" - {self.author}'
    
    def clean_text(self, text):
        """
        Clean the given text by replacing specific unicode characters with ASCII equivalents.

        Args:
            text (str): The text to be cleaned.

        Returns:
            str: The cleaned text with replacements made.
        """
        replacements = {
            '\u201c': '"',  # Left double quotation mark
            '\u201d': '"',  # Right double quotation mark
            '\u2018': "'",  # Left single quotation mark
            '\u2019': "'",  # Right single quotation mark
            # Add more replacements as needed
        }

        for old_char, new_char in replacements.items():
            text = text.replace(old_char, new_char)

        return text