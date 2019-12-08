from secrets import randbelow
from utils import read_keys_from_file, save_n_keys_to_file
import sys
from curve import EllipticCurve

SIZE = 64

HELP = """
  Diffy-Hellman protocol utility. Keys generator
  USAGE:
  python generate.py common_params.txt
  
  * common_params.txt file must include 6 values:
  p, a, b, Gx, Gy, n
  common_params.txt file_format - each key must be an integer number on a new line 

  * this utility creates private_key.txt & public_key.txt file. Don't share your private key with anybody!
"""
if len(sys.argv) < 2:
  print(HELP)

keys = read_keys_from_file(sys.argv[1])

if len(keys) < 6:
  print('not enougth keys')
  exit(1)

[p, a, b, Gx, Gy, n] = [int(k) for k in keys]

print(p, a, b, Gx, Gy, n, sep='\n')

d = randbelow(n)
while d == 0:
  d = randbelow(n)

print('d:', d)
curve = EllipticCurve(p, a, b, Gx, Gy)
Q = curve.exp(d)

save_n_keys_to_file('private_key.txt', [d])
save_n_keys_to_file('public_key.txt', Q)
print('Keys generated. See files: private_key.txt, public_key.txt')
