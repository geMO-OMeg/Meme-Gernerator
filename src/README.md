Meme Generator
Overview

The Meme Generator is a Python web application that enables users to create memes by either combining random quotes with images or by entering their own image URLs, quotes, and authors for personalized memes. The application supports multiple file formats for quote and image ingestion, and it allows image uploads via URLs or from a provided collection of quotes and images.

Features

    Generate memes using random quotes and images from a provided collection.
    Support for user-defined image URLs, quotes and authors.
    Ingest quotes from multiple file formats: TXT, CSV, DOCX, and PDF.
    Ingest images from multiple file formats: JPG, JPEG, PNG
    A simple web interface built with Flask.

Dependencies

Before running the application, ensure you have the following Python libraries installed:

    Flask
    requests
    PyPDF2
    python-docx
    Pillow

You can install the required packages using pip:
    pip install Flask requests PyPDF2 python-docx Pillow

Run the Application:

Start the Flask development server:
    flask run --host 0.0.0.0 --port 3000 --reload

The application will be available at http://127.0.0.1:3000


Sub-Modules Overview

Ingestor Interface

    Role: Defines the contract for all ingestor classes that handle different file types.
    Responsibilities: verifies if a file can be ingested then parses the file
    Example Usage:

    from .ingestor import IngestorInterface

Ingestor

    Role: Implements the main functionality to determine the appropriate ingestor for a given file type.
    Responsibilities: Utilizes specific ingestors (CSV, DOCX, PDF, TXT) to parse quote files. Additionally, the clean_text() function addresses issues related to unencodable characters.
    Example Usage:

    quotes = Ingestor.parse('path/to/quotes.txt')

QuoteModel

    Role: Represents a quote with its body and author.
    Responsibilities: Provides methods for for replacing unencodable characters and formatting the quote as a string.
    Example Usage:

    quote = QuoteModel("Life is what happens", "John Doe")
    print(str(quote))  # Output: "Life is what happens" - John Doe

MemeEngine

    Role: Handles the creation of memes by combining images with quotes.
    Responsibilities: Loads images, resizes them, and draws the quote text before saving the final meme.
    Example Usage:

    meme = MemeEngine('./static')
    path = meme.make_meme(image_path, quote.body, quote.author)

Flask Application

    Role: Manages the web interface for user interactions.
    Responsibilities: Serves routes for generating random memes and handling user input for custom memes.
    Example Usage:
        Access the main page: GET /
        Submit a meme request: POST /create

Usage Examples

    Generate a Random Meme: Access the root URL to generate a meme with random content.
    Create a Custom Meme: Use the form at /create to input an image URL, quote body, and author.


Create Function 

    Designed to generate a random image when no URL is provided and to select a random quote if neither a quote nor an author is specified. If a quote is submitted without an accompanying author, the system will search for a matching quote and use the corresponding author if found; otherwise, the author will be set to an empty string. Conversely, if an author is provided without a quote, the system will look for quotes attributed to that author. If a match is found, the quote will be returned; if not, the quote will also be set to an empty string.