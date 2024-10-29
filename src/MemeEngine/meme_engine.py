"""
Meme Engine Module.

This module provides the MemeEngine class, which is responsible for 
generating memes from images. The class allows users to create memes 
by adding quotes and authors to specified images, resizing the images 
while maintaining aspect ratios, and saving the final memes to a 
designated output directory.

Classes:
- MemeEngine: A class that handles meme generation by loading images, 
  drawing text on them, and saving the results to an output directory.

Usage:
To create a meme, initialize an instance of the MemeEngine with the 
desired output directory, then call the `make_meme` method with the 
image path, quote text, and author. The generated meme will be saved 
in the specified output directory.
"""

from PIL import Image, ImageDraw, ImageFont
import os


class MemeEngine:
    """
    A class for generating memes from images.

    This class handles the creation of memes by loading an image,
    resizing it, drawing a specified quote and author on it, and
    saving the final meme to a specified output directory.

    Attributes:
        output_dir (str): The directory where generated memes will be saved.
    """

    def __init__(self, output_dir: str):
        """
        Initialize the MemeEngine with the specified output directory.

        Args:
            output_dir (str): The directory where memes will be saved.
            If the directory does not exist, it will be created.
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """
        Create a meme from a specified image by adding a quote and author.

        This method opens the image, resizes it while maintaining the aspect
        ratio, and draws the specified quote and author onto the image. 
        The final meme is saved to the output directory.

        Args:
            img_path (str): The path to the input image file.
            text (str): The quote text to be drawn on the meme.
            author (str): The author of the quote to be included in the meme.
            width (int, optional): The desired width of the output meme.
                                   Defaults to 500 pixels.

        Returns:
            str: The file path to the saved meme image.

        Raises:
            IOError: If the input image cannot be opened or the output
                      directory cannot be written to.
        """
        # Load the image
        img = Image.open(img_path)

        # Resize the image while maintaining the aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(width * aspect_ratio)
        img = img.resize((width, new_height))

        # Prepare to draw on the image
        draw = ImageDraw.Draw(img)

        # Load a default font
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except IOError:
            font = ImageFont.load_default()

        # Prepare the text to be drawn
        full_text = f"{text}\n- {author}"
        text_width, text_height = draw.textsize(full_text, font=font)

        # Calculate text position (centered)
        text_x = (img.width - text_width) / 2
        text_y = img.height - text_height - 10  # 10 pixels from the bottom

        # Draw the text onto the image
        draw.text((text_x, text_y), full_text, font=font, fill="white")

        # Save the manipulated image
        output_path = os.path.join(self.output_dir, "meme.png")
        img.save(output_path)

        return output_path