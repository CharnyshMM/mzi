from hashlib import md5
from utils import read_key_from_file, save_key_to_file
import sys

HELP = """
    HMAC Utility.
    USAGE: python hmac.py file_to_check.txt private_key_file.bin [file_with_hash_to_compare_with.bin]

    * if "file_with_hash_to_compare_with.bin" is not provided, then value of HMAC function
    for "file_to_check.txt" will be saved to "file_hash.bin"

    ***********************************************
    To generate a key use keygen.py:
    $ python keygen.py 
"""

K = 123 # secret key

 # ipad = [ '\x36' * block_size ]
    # // оператор "*" указывает количество повторений последовательности байт,
    # // а block_size - размер блока хеш-функции, 
    # opad = [ '\x5c' * block_size ]
    
    # ikeypad = ipad ⊕ key
    # // оператор "⊕" выполняет побитовое исключающее ИЛИ (xor)
    # okeypad = opad ⊕ key
    
    # RETURN hash( okeypad ∥ hash( ikeypad ∥ msg ) )
    # // Оператор "∥" выполняет склейку строк

def hmac(key, msg):
    # key & message are expected to be bytearrays
    hash = md5()
    BLOCK_SIZE = hash.block_size
    if len(key) > BLOCK_SIZE:
        key = hash.update(key).digest 
    
    if len(key) < BLOCK_SIZE:
        key = key + bytearray([0]*(BLOCK_SIZE))

    ipad = [0x36] * BLOCK_SIZE
    opad = [0x5c] * BLOCK_SIZE

    ikeypad = [ipad[i] ^ key[i] for i in range(BLOCK_SIZE)]
    okeypad = [opad[i] ^ key[i] for i in range(BLOCK_SIZE)]

    h1 = md5()
    h1.update(bytearray(ikeypad) + msg) 
    h2 = md5()
    h2.update(bytearray(okeypad) + h2.digest())
    return h2.digest()

# def run(generate_key):
#     message = "1234567812345678901234567890"
#     message_b = bytearray(message, "utf-8")
#     # just a test of coverting to & from bytes :)
    
#     key = bytearray(int.to_bytes(int_key, byteorder='big', signed=False, length=64))
    
#     h1 = hmac(message_b, key)
#     print(len(h1))
#     print(int.from_bytes(h1, byteorder='big', signed=False))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(HELP)
        exit(0)
    
    file_to_test = sys.argv[1]
    print(file_to_test)
    key_file = sys.argv[2]
    print(key_file)
    file_with_hash_to_compare_with = None
    hash_to_compare_with = 0
    if len(sys.argv) == 4:
        file_with_hash_to_compare_with = sys.argv[3]
        hash_to_compare_with = read_key_from_file(file_with_hash_to_compare_with)

    key = bytearray(read_key_from_file(key_file))
    
    
    the_hash = 0
    with open(file_to_test, "r", encoding="utf-8") as f:
        message = f.read()
        the_hash = hmac(bytearray(message, "utf-8"), key)
    if file_with_hash_to_compare_with is not None:
        print('Hashes are equal' if the_hash == hash_to_compare_with else 'Hashes aren`t equal. Possibly file has been changed')
    else:
        save_key_to_file('file_hash.bin', the_hash)
        print('hash saved to file_hash.bin')