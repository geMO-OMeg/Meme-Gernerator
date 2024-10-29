"""
This module provides functionality to generate memes from quotes and images.

It allows users to create memes by either using a specified image path or 
selecting a random image from a predefined directory. Users can provide 
a quote body and author, or random quotes will be selected from specified 
files. The generated meme is saved to a temporary directory.

Functions:
- generate_meme: Generates a meme given an image path, quote body, and author.
"""

import os
import random
import argparse
from QuoteEngine.ingestor import Ingestor  # Ensure you import your Ingestor
from MemeEngine import MemeEngine  # Correct import
from QuoteEngine import QuoteModel  # Ensure you import QuoteModel


def generate_meme(path=None, body=None, author=None):
    """
    Generate a meme given an image path and a quote.

    This function creates a meme by either selecting a random image from a
    predefined directory or using a specified image path. It also selects a
    random quote if none is provided, or creates a QuoteModel object if a 
    quote body and author are specified.

    Args:
        path (str, optional): The path to the image file. If None, a random 
                              image will be selected from the default directory.
        body (str, optional): The quote body to be added to the meme. If None,
                              a random quote will be selected.
        author (str, optional): The author of the quote. This is required if 
                                a quote body is provided.

    Raises:
        Exception: If `body` is provided but `author` is None, an exception is 
                    raised indicating that the author is required.

    Returns:
        str: The file path to the generated meme image.
    """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv',
                   './_data/SimpleLines/SimpleLines.txt',
                   './_data/SimpleLines/SimpleLines.docx',
                   './_data/SimpleLines/SimpleLines.pdf',
                   './_data/SimpleLines/SimpleLines.csv',]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate a meme from a quote.")
    parser.add_argument('--path', type=str, help='Path to an image file')
    parser.add_argument('--body', type=str, help='Quote body to add to the image')
    parser.add_argument('--author', type=str, help='Quote author to add to the image')

    args = parser.parse_args()
    
    # Generate and print the meme path
    try:
        meme_path = generate_meme(args.path, args.body, args.author)
        print(f"Meme generated at: {meme_path}")
    except Exception as e:
        print(f"Error: {e}")

