import math
import random

lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
    , 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179
    , 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269
    , 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367
    , 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461
    , 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571
    , 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661
    , 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773
    , 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883
    , 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def sieve_atkin(limit):
    sieve = [False] * (limit + 1)
    if limit >= 2:
        sieve[2] = True
    if limit >= 3:
        sieve[3] = True
    for x in range(1, int(math.sqrt(limit)) + 1):
        for y in range(1, int(math.sqrt(limit)) + 1):
            n = 4 * x ** 2 + y ** 2
            if n <= limit and (n % 12 == 1 or n % 12 == 5): sieve[n] = not sieve[n]
            n = 3 * x ** 2 + y ** 2
            if n <= limit and n % 12 == 7: sieve[n] = not sieve[n]
            n = 3 * x ** 2 - y ** 2
            if x > y and n <= limit and n % 12 == 11: sieve[n] = not sieve[n]
    for x in range(5, int(math.sqrt(limit))):
        if sieve[x]:
            for y in range(x ** 2, limit + 1, x ** 2):
                sieve[y] = False
    return sieve


def primes_from_sieve(sieve):
    p = []
    for x in range(2, len(sieve)):
        if sieve[x]: p.append(x)
    return p


def is_square(n):
    return isqrt(n) ** 2 == n


def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def rabin_miller(n, iterations=40):
    s = n - 1
    t = 0
    while s & 1 == 0:
        s /= 2
        t += 1
    for _ in range(iterations):
        a = random.randrange(2, n - 1)
        v = pow(a, s, n)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
    return True


def is_prime(n):
    if n == 2:
        return True
    if (n >= 3):
        if (n & 1 != 0):
            for p in lowPrimes:
                if (n == p):
                    return True
                if (n % p == 0):
                    return False
            return rabin_miller(n)
    return False


def gen_prime(bits=1024):
    r = int(100 * (math.log(bits, 2) + 1))  # number of attempts max
    for x in range(r):
        n = random.randrange(2 ** (bits - 1), 2 ** (bits))
        if is_prime(n) == True:
            return n
    return None  # failed :(


def append_key(m, key, amt=1):
    if key in m:
        m[key] += amt
    else:
        m[key] = amt
    return m


def merge_maps(m1, m2):
    if 'unfactored' in m2:
        if 'unfactored' in m1:
            merge_maps(m1['unfactored'], m2['unfactored'])
        else:
            m1['unfactored'] = m2['unfactored']
    for key in m2:
        if key != 'unfactored':
            append_key(m1, key, m2[key])
    if 'unfactored' in m1 and len(m1['unfactored']) == 0:
        del m1['unfactored']
    return m1


def small_prime_factors(n, factors=None):
    if factors is None:
        factors = {}
    if n == 2:
        return append_key(factors, 2)
    for x in range(2, int(math.sqrt(n)) + 1):
        if n % x == 0:
            return small_prime_factors(n // x, append_key(factors, x))
    return append_key(factors, n)


def simple_factor(n, factors=None):
    if factors is None:
        factors = {}
        factors['unfactored'] = {}
    if is_prime(n):
        append_key(factors, n)
    else:
        print "Attempting to factor (%i)" % n
        # check for low factors
        for p in lowPrimes:
            if n%p==0:
                print "(%i) has a small prime factor" % n
                return merge_maps(append_key(factors, p), simple_factor(n // p))

        # if n is small, just brute force its factors
        bits = math.log(n, 2)
        if bits <= 48:
            print "(%i) is small! Brute forcing factors..." % n
            return merge_maps(small_prime_factors(n), factors)

        # check for squared, twin,cousin,sexy prime factors
        for diff in range(100):
            if is_square(n + diff ** 2):
                root = isqrt(n + diff ** 2)
                p = root - diff
                q = root + diff
                print "(%i) had 2 prime factors (%i) apart" % (n, 2 * diff)
                return merge_maps(simple_factor(p), simple_factor(q))
        print "Failed to automatically factor! http://factordb.com/index.php?query=%i" % n
        print "Try checking factorDB: "
        if bits <= 300:
            print """
            You should be able to factor this number with GGNFS/MSieve/YAFU if you have a decent computer (<=300 bits).
            """
        elif bits<=550:
            print """
            This number will require a lot of computing power to factor. (300 < bits <= 550)
            Try looking for patterns in various bases that might help you factor it mathematically.
            """
        else:
            print "This number will be very difficult to factor (bits > 550). You will likely need some factoring trick."
        if 'unfactored' in factors:
            append_key(factors['unfactored'], n)
            return factors
        else:
            factors['unfactored'] = {}
            append_key(factors['unfactored'], n)
            return factors
    return factors