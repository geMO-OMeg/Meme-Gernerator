import random
import os
import requests
from flask import Flask, render_template, abort, request
from meme import generate_meme
from QuoteEngine import Ingestor  # Ensure your Ingestor class is correctly imported
from MemeEngine import MemeEngine  # Ensure your MemeEngine class is correctly imported
from QuoteEngine.models import QuoteModel  # Ensure your QuoteModel is imported

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)
meme = MemeEngine('./static')
error_file = './_data/errorFile.txt'
temp_dir = './tmp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

"""
The setup function reads quotes from the specified files and collects all image paths from the ./_data/photos/dog/ directory.
It filters for image files with common extensions (jpg, jpeg, png).

The / route randomly selects an image and a quote, generates a meme, and renders it in meme.html.
The meme_rand function uses the random library to choose a quote and an image.

The /create route with GET method serves a form for user input.
The POST version of /create receives the image URL, body, and author from the form, saves the image locally, 
generates a meme, and deletes the temporary image file.

The Flask app runs in debug mode, which is useful for development.
"""

def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv',
                   './_data/SimpleLines/SimpleLinesTXT.txt',
                   './_data/SimpleLines/SimpleLinesDOCX.docx',
                   './_data/SimpleLines/SimpleLinesPDF.pdf',
                   './_data/SimpleLines/SimpleLinesCSV.csv',]

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    for file in quote_files:
        quotes.extend(Ingestor.parse(file))

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = [os.path.join(images_path, img) for img in os.listdir(images_path) if img.endswith(('.jpg', '.jpeg', '.png'))]
    with open(error_file, 'a') as f:
                f.write(f"images: {imgs}")
    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    # Select a random image and quote
    img = random.choice(imgs)
    quote = random.choice(quotes)
    
    # Generate the meme
    path = meme.make_meme(img, quote.body, quote.author)
    
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    image_url = request.form.get('image_url')
    body = request.form.get('body')
    author = request.form.get('author')

    if not image_url:
        img = random.choice(imgs)
        temp_image_path = None
    else:
        # Save the image from the image_url to a temp local file
        response = requests.get(image_url)
        temp_image_path = os.path.join(temp_dir, 'temp_image.jpg')  # Temporary image path

        try:
            with open(temp_image_path, 'wb') as f:
                f.write(response.content)
        except Exception as ex:
            with open(error_file, 'a') as f:
                f.write(f"\nwith open error, app.py: {ex}")
    
    if not body and not author:
        quote = random.choice(quotes)

    elif body and not author:
        matching_body = [q for q in quotes if q.body.lower() == body.lower()]
        if matching_body:
            quote = matching_body[0]  # Take the first matching quote
            author = quote.author  # Use the matched quote's body
        else:
            author=""  # No match found
        
    elif author and not body:
        matching_author = [q for q in quotes if q.author.lower() == author.lower()]
        if matching_author:
            quote = matching_author[0]  # Take the first matching quote
            body = quote.body  # Use the matched quote's body
        else:
            body=""  # No match found

        
    # Generate a meme using the temp file and the body and author
    if temp_image_path is None:
        path = meme.make_meme(img, body, author)
    else:
        path = meme.make_meme(temp_image_path, body, author)
        # Remove the temporary saved image
        os.remove(temp_image_path)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run(debug=False)




