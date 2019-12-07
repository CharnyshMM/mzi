from random import randint
from utils import save_key_to_file, read_key_from_file

key = bytearray([randint(0, 255) for _ in range(64)])
# int_key = int.from_bytes(key, byteorder='big', signed=False)

save_key_to_file('private_key.bin', key)
print('key saved to private_key.bin')
