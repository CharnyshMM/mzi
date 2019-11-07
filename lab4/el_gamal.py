import random
import sys
import math
import utils

R_LO, R_HI = 100, 2000
RANDOM_NUMBERS_FILE = "primes.txt"
PUBLIC_KEYS_FILE = 'public_keys.txt'
PRIVATE_KEYS_TXT = 'private_key.txt'
ENCRYPTED_TXT = 'encrypted.txt'
DECRYPTED_TXT = 'decrypted.txt'
HELP_TEXT = """
    USAGE: 

    * encryption: python el_gamal.py enc filename_to_read [filename_to_take_keys_from]
    * decryption: python el_gamal.py dec filename_to_read filename_to_take_keys_from

    - data to process is read from filename_to_read file as unicode string
    - if you do not specify a filename_to_take_keys_from on encryption operation, 
    then the script will generate public_keys.txt and private_keys.txt automatically.

    keys file format is (two ints separated with linebreak):
    1628537
    1331305

    the 1st int number is Module, the 2nd is public or private exponent
"""


def modular_exponentation(base, power, m):
    result = 1
    for _ in range(power):
        result = (result * base) % m
    return result


def get_prime_number_p():
    rand = random.randint(R_LO, R_HI)

    line = ""
    with open(RANDOM_NUMBERS_FILE, "r") as f:
        for _ in range(rand):
            line = f.readline()

    return int(line)


def get_prime_factors(num):
    prime_factors = []
    while not num % 2:
        prime_factors.append(2)
        num /= 2

    for i in range(3, int(math.sqrt(num)) + 1, 2):
        while not num % i:
            prime_factors.append(i)
            num /= i
    return prime_factors


def get_primitive_root_modulo(p, prime_factors):
    g = random.randint(2, p - 1)
    for i in range(len(prime_factors)):
        if modular_exponentation(g, (p - 1) / prime_factors[i], p) == 1:
            return get_primitive_root_modulo(p, prime_factors)
    return g


def euclidean_greatest_common_divisor(a, b):
    if b == 0:
        return a
    else:
        return euclidean_greatest_common_divisor(b, a % b)


def get_k(p):
    while True:
        k = random.randint(1, p - 1)
        if euclidean_greatest_common_divisor(k, p - 1) == 1:
            return k


def generate_keys():
    p = get_prime_number_p()

    g = get_primitive_root_modulo(p, get_prime_factors(p))

    x = random.randint(2, p - 1)
    y = modular_exponentation(g, x, p)

    print(
        f"""
  PUBLIC KEYS:
    p = {p}
    g = {g}
    y = {y}
  """
    )

    print(
        f"""
  SECRET KEY
    p = {p} 
    x = {x}
  """
    )

    return (p, g, y), x


def encrypt_char(ch, p, g, y):
    k = get_k(p)
    char_code = ord(ch)
    a = modular_exponentation(g, k, p)
    b = y ** k * char_code
    b = b % p  # not optimized
    return a, b

def encypt(message, p, g, y):
    encrypted_message = []
    for m in message:
        a, b = encrypt_char(m, p, g, y)
        encrypted_message.append(a)
        encrypted_message.append(b)
    return encrypted_message

def decrypt_char(a, b, p, x):
    return chr((b * (a ** (p - 1 - x))) % p)

def decrypt(int_message, p, x):
    decrypted_chars = []
    for i in range(0, len(int_message) - 1, 2):
        a = int_message[i]
        b = int_message[i + 1]

        m = decrypt_char(a, b, p, x)
        decrypted_chars.append(m)
    return decrypted_chars


def demo():
    (p, g, y), private_x = generate_keys()
    # message = [4]
    message = input('type in any text to encrypt: ')
    message_chars = []
    for m in message:
        message_chars.append(ord(m))
    print("message:\n", message_chars)

    encrypted = encypt(message, p, g, y)

    print("Encrypted:\n", encrypted)

    decrypted = decrypt(encrypted, p, private_x)
    print("Decrypted:\n", "".join(decrypted))


def main():
    if len(sys.argv) <= 2 and sys.argv[1] != 'demo':
        print(HELP_TEXT)
        exit(0)
    
    if sys.argv[1] == 'demo':
        demo()
        exit(0)
        

    encrypt_decrypt_command = sys.argv[1]
    file_to_read = sys.argv[2]
        
    p, g, y = None

    if encrypt_decrypt_command == 'enc':
        encrypted_message = []
        if len(sys.argv) < 4:
            (p, g, y), private_x = generate_keys()
            utils.save_keys_to_file(PUBLIC_KEYS_FILE, p, g, y)
            utils.save_keys_to_file(PRIVATE_KEYS_TXT, p, private_x)
        else:
           p, g, y = utils.read_n_keys_from_file(sys.argv[3], 3) 

        with open(file_to_read, 'r', encoding="utf-8") as f:
            while True:
                char  = f.read(1)
                if not char:
                    break
                a, b = encrypt_char(char, p, g, y)
                encrypted_message.append(f"{a} {b}")
        utils.save_chars_to_file('encrypted.txt', encrypted_message, separator="\n")
        exit(0)
      
    
    if len(sys.argv) < 4:
        raise Exception('no keys file specified to decrypt')

    decypted_message = []
    p, x = utils.read_n_keys_from_file(sys.argv[3], 2)

    with open(file_to_read, 'r') as f:
        while True:
            line  = f.readline()
            if not line:
                break
            a, b = line.split(" ")
            decypted_message.append(decrypt_char(int(a), int(b), p, x))

    
    utils.save_chars_to_file('decrypted.txt', decypted_message)


if __name__ == "__main__":
    main()

