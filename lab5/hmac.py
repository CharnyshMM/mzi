import hashlib

K = 123 # secret key
hash # 

BLOCK_SIZE = 8
def hmac(key, msg):
    if len(key) > BLOCK_SIZE:
        key = hash(key) 
    
    if len(key) < BLOCK_SIZE:
        key = key + "0"*(BLOCK_Slen(key))

    ipad = [0x36] * BLOCK_SIZE
    opad = [0x5c] * BLOCK_SIZE

    ikeypad = [ipad[i] ^ key[i] for i in range(BLOCK_SIZE)]
    okeypad = [opad[i] ^ key[i] for i in range(BLOCK_SIZE)]

    # ipad = [ '\x36' * block_size ]
    # // оператор "*" указывает количество повторений последовательности байт,
    # // а block_size - размер блока хеш-функции, 
    # opad = [ '\x5c' * block_size ]
    
    # ikeypad = ipad ⊕ key
    # // оператор "⊕" выполняет побитовое исключающее ИЛИ (xor)
    # okeypad = opad ⊕ key
    
    # RETURN hash( okeypad ∥ hash( ikeypad ∥ msg ) )
    # // Оператор "∥" выполняет склейку строк
    return hash()
    
