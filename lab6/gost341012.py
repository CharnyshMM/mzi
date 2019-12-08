from secrets import randbits

from utils import to_int
from utils import to_bytes
from utils import modular_invert


SIZE = 64


class EllipticCurve:
    def __init__(self, p, q, a, b, x, y):
        self.p = p # простое число, модуль элл кривой
        self.q = q # простое число от 2 в 254 до 2 в 256
        self.a = a # коеффициенты эллептич кривой
        self.b = b # коеффициенты эллептич кривой
        self.x = x  # точка на кривой
        self.y = y

    def pos(self, v):
        if v < 0:
            return v + self.p
        return v

    def add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * modular_invert(2 * p1y, self.p)) % self.p
        else:
            tx = self.pos(p2x - p1x) % self.p
            ty = self.pos(p2y - p1y) % self.p
            t = (ty * modular_invert(tx, self.p)) % self.p
        tx = self.pos(t * t - p1x - p2x) % self.p
        ty = self.pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def exp(self, d, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        d -= 1
        
        while d != 0:
            if d & 1 == 1:
                tx, ty = self.add(tx, ty, x, y)
            d = d >> 1
            x, y = self.add(x, y, x, y)
        return tx, ty


def generate_public_key(curve, prv):
    return curve.exp(prv)


def sign(E_curve, private_key, message):
    size = 64
    q = E_curve.q
    e = to_int(message) % q
    if e == 0:
        e = 1
    while True:
        k = (randbits(size*8)) % q  # сгенерировать псевдослуч целое К, 0 < k < q
        if k == 0:
            continue
        r, _ = E_curve.exp(k)  # вычислить икс координату точки С эллептич кривой: С = К*Р
        r %= q
        if r == 0:  # если == 0, то перегенерить К и повторить
            continue
        d = private_key * r 
        k *= e 
        s = (d + k) % q
        if s == 0:
            continue
        break
    # цифровая подпись = конкатенация двоичных векторов, соответствующих г и ЭС
    return r, s


def verify(curve, public_key, message, signature):
    r, s = signature

    if len(to_bytes(s, SIZE) + to_bytes(r, SIZE)) != SIZE * 2:
        raise ValueError("Invalid signature length")
    q = curve.q
    p = curve.p
    
    if r <= 0 or r >= q or s <= 0 or s >= q:
        return False
    e = to_int(message) % curve.q # bytes2long(digest) это альфа - число, соответствующее вектору хэшу полученного сообщения
    if e == 0:
        e = 1
    v = modular_invert(e, q) 
    z1 = s * v % q
    z2 = q - r * v % q
    # вычисляем точку С эллиптической кривой z1 * P + z2 * Q
    p1x, p1y = curve.exp(z1)
    q1x, q1y = curve.exp(z2, public_key[0], public_key[1])
    cx = q1x - p1x
    if cx < 0:
        cx += p
    cx = modular_invert(cx, p)
    z1 = q1y - p1y
    cx = cx * z1 % p
    cx = cx * cx % p
    cx = cx - p1x - q1x
    cx = cx % p
    if cx < 0:
        cx += p
    cx %= q
    return cx == r


def prv_unmarshal(prv):
    return to_int(prv[::-1])


def pub_marshal(pub):
    return (to_bytes(pub[1], SIZE) + to_bytes(pub[0], SIZE))[::-1]


def pub_unmarshal(pub, mode=2012):
    pub = pub[::-1]
    return to_int(pub[SIZE:]), to_int(pub[:SIZE])
