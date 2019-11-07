import random
import sys


R_LO, R_UP = 500, 2000
RANDOM_NUMBERS_FILE = 'primes.txt'
PRIVATE_KEYS_FILE = "private_keys.txt"
PUBLIC_KEYS_FILE = "public_keys.txt"
HELP_TEXT = """
    USAGE: 

    * encryption: python rsa.py enc filename_to_read [filename_to_take_keys_from]
    * decryption: python rsa.py dec filename_to_read filename_to_take_keys_from

    - data to process is read from filename_to_read file as unicode string
    - if you do not specify a filename_to_take_keys_from on encryption operation, 
    then the script will generate public_keys.txt and private_keys.txt automatically.

    keys file format is (two ints separated with linebreak):
    1628537
    1331305

    the 1st int number is Module, the 2nd is public or private exponent
"""



def save_keys_to_file(filename, k1, k2):
     with open(filename, 'w') as f:
        f.write(f'{str(k1)}\n')
        f.write(f'{str(k2)}\n')

def save_chars_to_file(filename, chars_list, separator=None):
    with open(filename, "w") as f:
        for char in chars_list:
            f.write(str(char))
            if (separator):
                f.write(separator)


def read_2_keys_from_file(filename):
    with open(filename, "r") as f:
        key1 = int(f.readline())
        key2 = int(f.readline())
        return key1, key2

def euclidean_greatest_common_divisor(a, b):
    if (b == 0):
        return a
    else:
        return euclidean_greatest_common_divisor(b, a % b)

def extended_euclidean_greatest_common_divisor(a, b):
    x, old_x = 0, 1
    y, old_y = 1, 0

    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y


def modular_exponentation(base, power, m):
    result = 1
    for _ in range(power):
        result = (result * base) % m
    return result


def choose_public_exponent(totient):
    while (True):
        e = random.randrange(2, totient)
        if (euclidean_greatest_common_divisor(e, totient) == 1):
            return e

def chooseKeys():
    rand1 = random.randint(R_LO, R_UP)
    rand2 = random.randint(R_LO, R_UP)
    while rand1 == rand2:
        rand2 = random.randint(R_LO, R_UP)

    lines = []
    with open(RANDOM_NUMBERS_FILE, 'r') as f:
        lines = f.readlines() 

    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1) 
    e = choose_public_exponent(totient)

    gcd, x, y = extended_euclidean_greatest_common_divisor(e, totient)

    if (x < 0):
        d = x + totient
    else:
        d = x
    
    return n, e, d

def encrypt_char(char, n_key, e_key):
    return modular_exponentation(ord(char), e_key, n_key)

def decrypt_char(char_code, n_key, d_key):
    return chr(modular_exponentation(char_code, d_key, n_key))


def demo():
    n_key, e_key, d_key = chooseKeys()
    message = input('Input some text: ')
    
    encrypted_message = []
    
    for char in message:
        encrypted_message.append(encrypt_char(char, n_key, e_key))

    print('Encrypted:', encrypted_message)

    decypted_message = []
    for char_code in encrypted_message:
        decypted_message.append(decrypt_char(char_code, n_key, d_key))
    print('Decrypted:',''.join(decypted_message))


def main():
    if len(sys.argv) <= 2 and sys.argv[1] != 'demo':
        print(HELP_TEXT)
        exit(0)
    
    if sys.argv[1] == 'demo':
        demo()
        exit(0)
        
    encrypt_decrypt_command = sys.argv[1]
    file_to_read = sys.argv[2]

    n_key = 0
    e_key = 0
    d_key = 0
        
    if encrypt_decrypt_command == 'enc':
        encrypted_message = []
        if len(sys.argv) < 4:
            n_key, e_key, d_key = chooseKeys()
        else:
           n_key, e_key = read_2_keys_from_file(sys.argv[3]) 

        with open(file_to_read, 'r') as f:
            while True:
                char  = f.read(1)
                if not char:
                    break
                encrypted_message.append(encrypt_char(char, n_key, e_key))
        save_chars_to_file('encrypted.txt', encrypted_message, separator=" ")
        exit(0)
      
    
    if len(sys.argv) < 4:
        raise Exception('no keys file specified to decrypt')

    decypted_message = []
    n_key, d_key = read_2_keys_from_file(sys.argv[3])

    with open(file_to_read, 'r') as f:
        next_char_code = ""
        while True:
            char  = f.read(1)
            if not char:
                break
            if char == " " and len(next_char_code) > 0:
                decypted_message.append(decrypt_char(int(next_char_code), n_key, d_key))
                next_char_code = ""
            else:
                next_char_code += char
    
    save_chars_to_file('decrypted.txt', decypted_message)


if __name__ == "__main__":
    demo()
