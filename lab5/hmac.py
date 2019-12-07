from hashlib import md5
import random

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

def run():
    message = "1234567812345678901234567890"
    message_b = bytearray(message, "utf-8")
    # just a test of coverting to & from bytes :)
    key = bytearray([random.randint(0, 255) for i in range(64)])
    int_key = int.from_bytes(key, byteorder='big', signed=False)
    key = bytearray(int.to_bytes(int_key, byteorder='big', signed=False, length=64))
    
    h1 = hmac(message_b, key)
    print(len(h1))
    print(int.from_bytes(h1, byteorder='big', signed=False))

if __name__ == "__main__":
    run()