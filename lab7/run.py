from secrets import randbits
from utils import read_keys_from_file, save_n_keys_to_file
import sys
from curve import EllipticCurve

SIZE = 64

HELP = """
  Diffie–Hellman protocol utility common_params.txt your_private_key.txt other_user_public_key.txt

  [1]  common_params.txt - file with common params p, a, b, Gx, Gy (Ell.curve initialisation)
  [2]  your_private_key.txt - YOUR private key
  [3]  other_user_public_key.txt - OTHER USER public key. Other user is someone you want to communicate to using Diffie–Hellman protocol

  the output of this utility is your common secret key you may use for symmetryc cryptography
  it is saved to symmetric_key.txt file
"""

if len(sys.argv) < 4:
  print(HELP)
  exit(0)

common_keys = read_keys_from_file(sys.argv[1])

if len(common_keys) < 6:
  print('not enougth keys')
  exit(1)

[p, a, b, Gx, Gy, n] = [int(k) for k in common_keys]

d = read_keys_from_file(sys.argv[2])[0]
d = int(d)

curve = EllipticCurve(p, a, b, Gx, Gy)


Q = read_keys_from_file(sys.argv[3])

x, _ = curve.exp(d, int(Q[0]), int(Q[1]))
print('common secret: ', x)
save_n_keys_to_file('symmetric_key.txt', [x])


