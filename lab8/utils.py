import numpy as np
from skimage.util import view_as_blocks
from scipy.fftpack import dct, idct
from params import *

def to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        result.extend(map(int, bits.rjust(8, '0')))
    return result


def from_bits(bits):
    chars = []
    for i in range(len(bits) // 8):
        byte_char = bits[i * 8:(i + 1) * 8]
        int_char = int(''.join(map(str, byte_char)), 2)
        chars.append(chr(int_char))
    return ''.join(chars)



def double_to_byte(arr):
    return np.uint8(np.round(np.clip(arr, 0, 255), 0))


def increment_abs(x):
    return x + 1 if x >= 0 else x - 1


def decrement_abs(x):
    if np.abs(x) <= 1:
        return 0
    else:
        return x - 1 if x >= 0 else x + 1


def abs_diff_coeffs(transform):
    return abs(transform[u1, v1]) - abs(transform[u2, v2])


def valid_coeffs(transform, bit, threshold):
    difference = abs_diff_coeffs(transform)
    if (bit == 0) and (difference > threshold):
        return True
    elif (bit == 1) and (difference < -threshold):
        return True
    else:
        return False


def change_coeffs(transform, bit):
    coefs = transform.copy()
    if bit == 0:
        coefs[u1, v1] = increment_abs(coefs[u1, v1])
        coefs[u2, v2] = decrement_abs(coefs[u2, v2])
    elif bit == 1:
        coefs[u1, v1] = decrement_abs(coefs[u1, v1])
        coefs[u2, v2] = increment_abs(coefs[u2, v2])
    return coefs

