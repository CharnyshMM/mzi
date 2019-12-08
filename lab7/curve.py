from utils import modular_invert
SIZE = 64


class EllipticCurve:
    def __init__(self, p, a, b, x, y):
        self.p = p # простое число, модуль элл кривой
        self.a = a # коеффициенты эллептич кривой
        self.b = b # коеффициенты эллептич кривой
        self.x = x
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
