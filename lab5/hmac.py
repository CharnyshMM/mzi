from hashlib import md5

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
        key = hash(key) 
    
    if len(key) < BLOCK_SIZE:
        key = key + "0"*(BLOCK_Slen(key))

    ipad = [0x36] * BLOCK_SIZE
    opad = [0x5c] * BLOCK_SIZE

    ikeypad = [ipad[i] ^ key[i] for i in range(BLOCK_SIZE)]
    okeypad = [opad[i] ^ key[i] for i in range(BLOCK_SIZE)]

    h1.update(bytearray(ikeypad) + sb) 
    h2 = hashlib.md5()
    h2.update(bytearray(okeypad) + h2.digest())
    return h2.digest()

   
