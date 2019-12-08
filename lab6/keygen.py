from gost341012 import EllipticCurve, prv_unmarshal, generate_public_key
import os

KEY_LENGTH = 128

def generate_keys(curve):
    privkey = prv_unmarshal(os.urandom(KEY_LENGTH))
    pubkey = generate_public_key(curve, privkey)

    return pubkey, privkey
