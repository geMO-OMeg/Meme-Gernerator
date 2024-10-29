"""
This module provides a web application for generating memes.

It allows users to create memes by combining random quotes and images. 
The application can also generate memes based on user input, supporting
image uploads and custom quotes.

Modules:
- setup: Load resources for the meme application.
- meme_rand: Generate and render a random meme.
- meme_form: Render a form for user input.
- meme_post: Create and render a user-defined meme.
"""

import random
import os
import re
import requests
from flask import Flask, render_template, abort, request
from meme import generate_meme
from QuoteEngine import Ingestor  
from MemeEngine import MemeEngine  
from QuoteEngine.models import QuoteModel  

app = Flask(__name__)
meme = MemeEngine('./static')
temp_dir = './tmp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def setup():
    """Load all resources for the meme application.

    This function reads quotes from specified text files and collects image paths
    from the './_data/photos/dog/' directory. It filters for image files with 
    common extensions (jpg, jpeg, png).

    Returns:
        tuple: A tuple containing two lists:
            - List of QuoteModel instances.
            - List of image file paths.
    """
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv',
                   './_data/SimpleLines/SimpleLinesTXT.txt',
                   './_data/SimpleLines/SimpleLinesDOCX.docx',
                   './_data/SimpleLines/SimpleLinesPDF.pdf',
                   './_data/SimpleLines/SimpleLinesCSV.csv',]

    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(file))

    images_path = "./_data/photos/dog/"

    imgs = [os.path.join(images_path, img) for img in os.listdir(images_path) if img.endswith(('.jpg', '.jpeg', '.png'))]
    
    return quotes, imgs

quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate and render a random meme.

    This function selects a random image and a random quote from the pre-loaded
    lists, generates a meme using the MemeEngine, and renders the meme in 
    'meme.html'.

    Returns:
        str: The rendered HTML template with the generated meme path.
    """
    img = random.choice(imgs)
    quote = random.choice(quotes)
    
    path = meme.make_meme(img, quote.body, quote.author)
    
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """Render the form for user input.

    This function serves the HTML form that allows users to input their own
    meme parameters.

    Returns:
        str: The rendered HTML template for the meme input form.
    """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create and render a user-defined meme.

    This function processes the user's input from the form, either generating
    a meme from a provided image URL or selecting a random image if no URL is
    given. It can also fill in the quote or author based on user input.

    Returns:
        str: The rendered HTML template with the generated meme path.
    """
    image_url = request.form.get('image_url')
    body = request.form.get('body')
    if body in {'-', '', ' '}:
        body = None

    author = request.form.get('author')
    if author in {'-', '', ' '}:
        author = None

    if not image_url:
        img = random.choice(imgs)
        temp_image_path = None
    else:
        # Save the image from the image_url to a temp local file
        response = requests.get(image_url)
        temp_image_path = os.path.join(temp_dir, 'temp_image.jpg')

        try:
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
        except Exception as ex:
            print(f"\nwith open error, app.py: {ex}")

    # Generate a random quote if both body and author are None
    if body is None and author is None:
        quote = random.choice(quotes)
        body = quote.body
        author = quote.author
    else:
        if body and author is None:
            matching_body = [q for q in quotes if q.body.lower() == body.lower()]
            if matching_body:
                quote = matching_body[0] 
                author = quote.author  
            else:
                author = None 

        if author and body is None:
            matching_author = [q for q in quotes if q.author.lower() == author.lower()]
            if matching_author:
                quote = matching_author[0] 
                body = quote.body
            else:
                body = None

    # Generate a meme using the temp file and the body and author
    if temp_image_path is None:
        path = meme.make_meme(img, body, author)
    else:
        path = meme.make_meme(temp_image_path, body, author)
        os.remove(temp_image_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()




