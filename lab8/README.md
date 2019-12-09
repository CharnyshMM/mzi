# LAB 8

# Zhao-Koch's steganography algorithm realization

 - utility to write and read steganography from jpeg images
 
## Additional package required:

- [https://scikit-image.org/]() is used for reading, writing & modifying images
- you may either install the package manually or run
    
        $ pip install -r requirements.txt

## Usage:

1. write a text

        $ python write.py img_template.jpeg color_id

  color_id - the color channel your text will be inserted to.

   - ![#f03c15](https://placehold.it/15/f03c15/000000?text=+) `color_id = 0`
   - ![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `color_di = 1`
   - ![#1589F0](https://placehold.it/15/1589F0/000000?text=+) `color_id = 2`

2. read a text from file

        $ python read.py img_with_embedded_text.jpeg color_id [message_length]

  - img_with_embedded_text.jpeg - jpeg file with embedded text message
  - color_id - digit representing the color of RGB. Message text is mixed into the colors channel
      0 - Red
      1 - Green
      2 - Blue
  - message_length - is integer length of message (characters amount). If you don't know it you may omit this parameter. The app will display all bits that may possibly contain the information. If the image really contains embedded text, the text will be displayed first  (followed by some junky chars)
