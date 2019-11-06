import random
import math

RANDOM_NUMBERS_FILE = 'primes.txt'


def modular_exponentation(base, power, m):
    result = 1
    for _ in range(power):
        result = (result * base) % m
    return result


def get_prime_number_p():
  rand = random.randint(100, 10000)

  line = ""
  with open(RANDOM_NUMBERS_FILE, 'r') as f:
    for _ in range(rand):
      line = f.readline()

  return int(line)

def get_prime_factors(num):
  prime_factors = []
  while not num % 2:
    prime_factors.append(2)
    num /= 2
  
  for i in range(3, int(math.sqrt(num))+1, 2):
    while not num % i:
      prime_factors.append(i)
      num /= i
  return prime_factors


def get_primitive_root_modulo(p, prime_factors):
  g = random.randint(2, p - 1)
  for i in range(len(prime_factors)):
    if modular_exponentation(g, (p-1)/prime_factors[i], p) == 1:
      return get_primitive_root_modulo(p,prime_factors)
  return g

def euclidean_greatest_common_divisor(a, b):
    if (b == 0):
        return a
    else:
        return euclidean_greatest_common_divisor(b, a % b)


def get_k(p):
  while True:
    k = random.randint(1, p-1)
    if euclidean_greatest_common_divisor(k, p-1) == 1:
      return k

def generate_keys():
  p = get_prime_number_p()

  g = get_primitive_root_modulo(p, get_prime_factors(p))

  x = random.randint(2 ,p-1)
  y = modular_exponentation(g, x, p)

  print(f"""
  PUBLIC KEYS:
    p = {p}
    g = {g}
    y = {y}
  """)

  print(f"""
  SECRET KEY
    p = {p} 
    x = {x}
  """)

  return {"p": p, "g": g, "y": y}, x

def encypt(message, p, g, y):
  encrypted_message = []
  for m in message:
    k = get_k(p)
    char_code = ord(m)
    a = modular_exponentation(g, k, p)
    b = (y**k * char_code)
    b = b % p # not optimized
    encrypted_message.append(a)
    encrypted_message.append(b)
  return encrypted_message

def decrypt(int_message, p, x):
  decrypted_chars = []
  for i in range(0, len(int_message)-1, 2):
    a = int_message[i]
    b = int_message[i+1]

    m = (b*(a** (p - 1 - x))) % p
    decrypted_chars.append(chr(m))
  return decrypted_chars



def main():
  public_keys, private_key = generate_keys()
  # message = [4]
  message = "I love rock-n-roll"
  message_chars = []
  for m in message:
    message_chars.append(ord(m))
  print("message:\n", message_chars)

  encrypted = encypt(message, public_keys["p"], public_keys["g"], public_keys["y"])

  print("Encrypted:\n", encrypted)
  
  decrypted = decrypt(encrypted, public_keys["p"], private_key)
  print("Decrypted:\n", "".join(decrypted))

        
if __name__ == "__main__":
  main()