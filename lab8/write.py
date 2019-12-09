
from skimage.util import view_as_blocks
from utils import dct, idct, to_bits, valid_coeffs, change_coeffs, double_to_byte
from read import retrieve_bit
from skimage import io
from params import *
import sys

HELP = """
  Zhao-Koch's steganography algorithm realization. Message writer
  USAGE: 
  $ python write.py img_with_embedded_text.jpeg color_id [message_length]

  * image_template.jpeg - jpeg file to generate image with embedded text
  * color_id - digit representing the color of RGB. Message text is mixed into the colors channel
      0 - Red
      1 - Green
      2 - Blue
"""

def embed_bit(block, bit):
    patch = block.copy()
    coefs = dct(dct(patch, axis=0, norm='ortho'), axis=1, norm='ortho')
    while not valid_coeffs(coefs, bit, P) or (bit != retrieve_bit(patch)):
        coefs = change_coeffs(coefs, bit)
        patch = double_to_byte(idct(idct(coefs, axis=0, norm='ortho'), axis=1, norm='ortho'))
    return patch


def embed_message(orig, msg, color):
    changed = orig.copy()
    print(color)
    color_chanel = changed[:, :, color]
    blocks = view_as_blocks(color_chanel, block_shape=(N, N))
    h = blocks.shape[1]
    for index, bit in enumerate(msg):
        i = index // h
        j = index % h
        block = blocks[i, j]
        color_chanel[i * N: (i + 1) * N, j * N: (j + 1) * N] = embed_bit(block, bit)
    changed[:, :, color] = color_chanel
    return changed


if __name__ == "__main__":
    if len(sys.argv) < 2:
      print("help")
      exit(0)

    message = to_bits('my message')
    
    color = 0
    if len(sys.argv) == 3:
      color = int(sys.argv[2])
    if color > 2:
      print('ERROR: color must be 0, 1, 2.')
      exit(1)
    original_jpg = io.imread(sys.argv[1])
    img = embed_message(original_jpg, message, color)
    io.imsave('embedded.jpeg', img, quality=100)
    print('Saved to embedded.jpeg')

    