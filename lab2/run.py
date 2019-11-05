import binascii

class belt:
    def __init__(self, key):
        self.H = [0xB1, 0x94, 0xBA, 0xC8, 0x0A, 0x08, 0xF5, 0x3B, 0x36, 0x6D, 0x00, 0x8E, 0x58, 0x4A, 0x5D, 0xE4,
                  0x85, 0x04, 0xFA, 0x9D, 0x1B, 0xB6, 0xC7, 0xAC, 0x25, 0x2E, 0x72, 0xC2, 0x02, 0xFD, 0xCE, 0x0D,
                  0x5B, 0xE3, 0xD6, 0x12, 0x17, 0xB9, 0x61, 0x81, 0xFE, 0x67, 0x86, 0xAD, 0x71, 0x6B, 0x89, 0x0B,
                  0x5C, 0xB0, 0xC0, 0xFF, 0x33, 0xC3, 0x56, 0xB8, 0x35, 0xC4, 0x05, 0xAE, 0xD8, 0xE0, 0x7F, 0x99,
                  0xE1, 0x2B, 0xDC, 0x1A, 0xE2, 0x82, 0x57, 0xEC, 0x70, 0x3F, 0xCC, 0xF0, 0x95, 0xEE, 0x8D, 0xF1,
                  0xC1, 0xAB, 0x76, 0x38, 0x9F, 0xE6, 0x78, 0xCA, 0xF7, 0xC6, 0xF8, 0x60, 0xD5, 0xBB, 0x9C, 0x4F,
                  0xF3, 0x3C, 0x65, 0x7B, 0x63, 0x7C, 0x30, 0x6A, 0xDD, 0x4E, 0xA7, 0x79, 0x9E, 0xB2, 0x3D, 0x31,
                  0x3E, 0x98, 0xB5, 0x6E, 0x27, 0xD3, 0xBC, 0xCF, 0x59, 0x1E, 0x18, 0x1F, 0x4C, 0x5A, 0xB7, 0x93,
                  0xE9, 0xDE, 0xE7, 0x2C, 0x8F, 0x0C, 0x0F, 0xA6, 0x2D, 0xDB, 0x49, 0xF4, 0x6F, 0x73, 0x96, 0x47,
                  0x06, 0x07, 0x53, 0x16, 0xED, 0x24, 0x7A, 0x37, 0x39, 0xCB, 0xA3, 0x83, 0x03, 0xA9, 0x8B, 0xF6,
                  0x92, 0xBD, 0x9B, 0x1C, 0xE5, 0xD1, 0x41, 0x01, 0x54, 0x45, 0xFB, 0xC9, 0x5E, 0x4D, 0x0E, 0xF2,
                  0x68, 0x20, 0x80, 0xAA, 0x22, 0x7D, 0x64, 0x2F, 0x26, 0x87, 0xF9, 0x34, 0x90, 0x40, 0x55, 0x11,
                  0xBE, 0x32, 0x97, 0x13, 0x43, 0xFC, 0x9A, 0x48, 0xA0, 0x2A, 0x88, 0x5F, 0x19, 0x4B, 0x09, 0xA1,
                  0x7E, 0xCD, 0xA4, 0xD0, 0x15, 0x44, 0xAF, 0x8C, 0xA5, 0x84, 0x50, 0xBF, 0x66, 0xD2, 0xE8, 0x8A,
                  0xA2, 0xD7, 0x46, 0x52, 0x42, 0xA8, 0xDF, 0xB3, 0x69, 0x74, 0xC5, 0x51, 0xEB, 0x23, 0x29, 0x21,
                  0xD4, 0xEF, 0xD9, 0xB4, 0x3A, 0x62, 0x28, 0x75, 0x91, 0x14, 0x10, 0xEA, 0x77, 0x6C, 0xDA, 0x1D]
        key = [self.list2int(key[i:i+4]) for i in range(0, len(key), 4)]
        self.k = [key[i % 8] for i in range(56)]

    # RotHi operation
    def rotHi(self, value, k):
        bitlength = 32
        return (value << (k % bitlength) & 2 ** bitlength - 1) ^ (value >> (bitlength - k) % bitlength)

    # Represent 32-bit number as list of bytes
    def int2list(self, x):
        return [x >> i & 0xff for i in [24, 16, 8, 0]]

    # Represent list of bytes as 32-bit number
    def list2int(self, x):
        l = [24, 16, 8, 0]
        return sum([x[i] << l[i] for i in range(4)])

    # Modular Substraction
    def modular_subtract(self, x, y):
        mod = 2**32
        return (x - y) % mod

    # Modular addition
    def modular_addition(self, *x):
        mod = 2**32
        res = 0
        for el in x:
            res = (res + self.reverse(el)) % mod
        return self.reverse(res)

    # H-transformation: replacing byte with another value from table
    def h_transformation(self, x):
        return self.H[x]

    # G-transformation
    def g_transformation(self, x, k):
        res = self.list2int([self.h_transformation(i) for i in self.int2list(x)])
        return self.reverse(self.rotHi(self.reverse(res), k))

    # Reverse bytes in word x
    def reverse(self, x):
        l = self.int2list(x)
        l.reverse()
        return self.list2int(l)

    # Encrypt message with multiple blocks
    def encrypt_long(self, m):
        print(m)
        while len(m) % 16:
            m.append(0)
        
        result = []
        for i in range(0,len(m), 16):
            result.extend(self.encryption(m[i:i+16]))
        return result

    # Encrypt input m represented as list of bytes using key represented as list of bytes #64bytes
    def encryption(self, m):
        print([self.list2int(m[i:i+4]) for i in range(0, len(m), 4)])
        a, b, c, d = [self.list2int(m[i:i+4]) for i in range(0, len(m), 4)]
        for i in range(8):
            b = b ^ self.g_transformation(self.modular_addition(a, self.k[7*i+0]), 5)
            c = c ^ self.g_transformation(self.modular_addition(d, self.k[7*i+1]), 21)
            a = self.reverse(self.modular_subtract(self.reverse(a),
                                         self.reverse(self.g_transformation(self.modular_addition(b, self.k[7*i+2]), 13))))
            e = (self.g_transformation(self.modular_addition(b, c, self.k[7*i+3]), 21)) ^ self.reverse(i+1)
            b = self.modular_addition(b, e)
            c = self.reverse(self.modular_subtract(self.reverse(c), self.reverse(e)))
            d = self.modular_addition(d, self.g_transformation(self.modular_addition(c, self.k[7*i+4]), 13))
            b = b ^ self.g_transformation(self.modular_addition(a, self.k[7*i+5]), 21)
            c = c ^ self.g_transformation(self.modular_addition(d, self.k[7*i+6]), 5)
            a, b = b, a
            c, d = d, c
            b, c = c, b
        a = self.int2list(a)
        b = self.int2list(b)
        c = self.int2list(c)
        d = self.int2list(d)
        return b + d + a + c

    # Decrypt message with multiple blocks
    def decrypt_long(self, m):
        while len(m) % 16:
            m.append(0)
        result = []
        for i in range(0, len(m), 16):
            result.extend(self.encryption(m[i:i+16]))
        return result

    # Decrypt input m represented as list of bytes using key represented as list of bytes
    def decryption(self, m):
        a, b, c, d = [self.list2int(m[i:i+4]) for i in range(0, len(m), 4)]
        for i in reversed(range(8)):
            b = b ^ self.g_transformation(self.modular_addition(a, self.k[7*i+6]), 5)
            c = c ^ self.g_transformation(self.modular_addition(d, self.k[7*i+5]), 21)
            a = self.reverse(self.modular_subtract(self.reverse(a),
                                         self.reverse(self.g_transformation(self.modular_addition(b, self.k[7*i+4]), 13))))
            e = (self.g_transformation(self.modular_addition(b, c, self.k[7*i+3]), 21)) ^ self.reverse(i+1)
            b = self.modular_addition(b, e)
            c = self.reverse(self.modular_subtract(self.reverse(c), self.reverse(e)))
            d = self.modular_addition(d, self.g_transformation(self.modular_addition(c, self.k[7*i+2]), 13))
            b = b ^ self.g_transformation(self.modular_addition(a, self.k[7*i+1]), 21)
            c = c ^ self.g_transformation(self.modular_addition(d, self.k[7*i+0]), 5)
            a, b = b, a
            c, d = d, c
            a, d = d, a
        a = self.int2list(a)
        b = self.int2list(b)
        c = self.int2list(c)
        d = self.int2list(d)
        return c + a + d + b

################################################
# Таблица А.6 — Зашифрование в режиме простой замены
################################################

key = list(
  bytes.fromhex(
            "E9DEE72C8F0C0FA62DDB49F46F73964706075316ED247A3739CBA38303A98BF6"
        )
)

message = list(
        bytes.fromhex(
        #"B194BAC80A08F53B366D008E584A5DE4"
        "B194BAC80A08F53B366D008E584A5DE48504FA9D1BB6C7AC252E72C202FDCE0D5BE3D61217B96181FE6786AD716B890B"
      )
    )
b = belt(key)
#e = b.encryption(message)
e = b.encrypt_long(message)
print("result A6:")
print(["{:02x}".format(i) for i in e])

print("-"*50)
################################################
# Таблица А.7 — Зашифрование в режиме простой замены
################################################

key = list(
  bytes.fromhex(
            "E9DEE72C8F0C0FA62DDB49F46F73964706075316ED247A3739CBA38303A98BF6"
        )
)

message = list(
        bytes.fromhex(
        #"B194BAC80A08F53B366D008E584A5DE4"
        #"E12BDC1AE28257EC703FCCF095EE8DF1C1AB76389FE678CAF7C6F860D5BB9C4FF33C657B637C306ADD4EA7799EB23D31"
        "B194BAC80A08F53B366D008E584A5DE48504FA9D1BB6C7AC252E72C202FDCE0D5BE3D61217B96181FE6786AD716B89"
      )
    )
b = belt(key)
#e = b.encryption(message)
e = b.decrypt_long(message)
print("result A7:")
print(["{:02x}".format(i) for i in e])
