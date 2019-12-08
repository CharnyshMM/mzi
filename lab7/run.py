from secrets import randbits
from utils import read_keys_from_file
import sys
from curve import EllipticCurve

SIZE = 64

HELP = """
  Diffy-Hellman protocol utility
  [1] - common_params.txt
  [2] - private_key.txt
  [3] - other user public key
"""

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


