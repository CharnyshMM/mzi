def to_int(raw):
    return int.from_bytes(raw, byteorder="big", signed=False)


def to_bytes(n, size=32):
    return int.to_bytes(n, byteorder="big", length=size, signed=False)


def modular_invert(a, n):
    if a < 0:
        # k^-1 = p - (-k)^-1 mod p
        return n - modular_invert(-a, n)
    t, newt = 0, 1
    r, newr = n, a
    while newr != 0:
        quotinent = r // newr
        t, newt = newt, t - quotinent * newt
        r, newr = newr, r - quotinent * newr
    if r > 1:
        return -1
    if t < 0:
        t = t + n
    return t


def save_n_keys_to_file(filename, keys):
    with open(filename, 'w') as f:
        for k in keys:
            f.write(f"{k}\n")


def read_keys_from_file(filename):
    keys = []
    with open(filename, "rb") as f:
        line = f.readline()
        while line:
            keys.append(line)
            line = f.readline()
    return keys