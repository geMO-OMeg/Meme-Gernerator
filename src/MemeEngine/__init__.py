"""
Meme Engine Package.

This package provides the MemeEngine class for generating memes 
from images. It allows users to overlay quotes and authors on 
specified images, resize the images while maintaining aspect ratios, 
and save the final memes to a specified output directory.

Key Features:
- Create memes with custom quotes and authors.
- Automatically handle image resizing to fit specified dimensions.
- Save generated memes to a designated output location.

Usage:
To use this package, import the MemeEngine class and create an 
instance with the desired output directory. Use the `make_meme` 
method to generate and save memes.
"""

from .meme_engine import MemeEngine