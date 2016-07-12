def xgcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = xgcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


class RSAPrivateKey():
    def __init__(self, p, q, e=65537, n=None, d=None, phi=None, dp=None, dq=None, invq=None):
        #p should always be > q
        if q>p:
            temp = p
            p=q
            q=temp
        if n==None:
            n=p*q
        if phi==None:
            phi = (p-1)*(q-1)
        if d==None:
            d = modinv(e,phi)
        if dp==None:
            dp = d % (p-1)
        if dq==None:
            dq = d % (q-1)
        if invq==None:
            invq = modinv(q, p)
        self.q = q
        self.p = p
        self.e = e
        self.n = n
        self.d = d
        self.phi = phi
        self.dp = dp
        self.dq = dq
        self.invq = invq
    def __str__(self):
        return "(%i, %i)"%(self.p,self.q)
    def toPublicKey(self):
        return RSAPublicKey(self.e, self.n)

class RSAPublicKey():
    def __init__(self, e, n):
        self.e=e
        self.n=n