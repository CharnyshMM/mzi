from skimage.util import view_as_blocks
from utils import dct, abs_diff_coeffs, to_bits, from_bits
from params import N
from skimage.util import view_as_blocks
from skimage import io
import sys


HELP = """
  Zhao-Koch's steganography algorithm realization. Message reader
  USAGE: 
  $ python read.py img_with_embedded_text.jpeg color_id [message_length]

  * img_with_embedded_text.jpeg - jpeg file with embedded text message
  * color_id - digit representing the color of RGB. Message text is mixed into the colors channel
      0 - Red
      1 - Green
      2 - Blue
  * message_length - is integer length of message (characters amount). If you don't know it 
  you may omit this parameter. The app will display all bits that may possibly contain the information.
  The image really contains embedded text, the text will be displayed first  (followed by some junky chars)
"""

def retrieve_bit(block):
    transform = dct(dct(block, axis=0), axis=1)
    return 0 if abs_diff_coeffs(transform) > 0 else 1


def retrieve_message(img, length, c):
    print(c)
    blocks = view_as_blocks(img[:, :, c], block_shape=(N, N))
    h = blocks.shape[1]
    return [retrieve_bit(blocks[index//h, index%h]) for index in range(length)]


if __name__ == "__main__":
    if len(sys.argv) < 3:
      print(HELP)
      exit(0)
    color = int(sys.argv[2])

    img = io.imread(sys.argv[1])
    length = int(sys.argv[3]) * 8 if len(sys.argv) > 3 else len(img[:,:,color])
    bit_message = retrieve_message(img, length, color)
    print('Message:', from_bits(bit_message))
    