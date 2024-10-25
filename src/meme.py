import os
import random
from QuoteEngine.ingestor import Ingestor  # Ensure you import your Ingestor
from MemeEngine import MemeEngine  # Correct import
from QuoteEngine import QuoteModel  # Ensure you import QuoteModel

# @TODO Import your Ingestor and MemeEngine classes

error_file = './_data/errorFile.txt'

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
    
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    # add docstring
    
    args = None
    print(generate_meme(args.path, args.body, args.author))
