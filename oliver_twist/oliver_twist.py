#!/usr/bin/env python

import gmpy
import random
from Crypto.Util.number import *

def tosh(n, p):
    if pow(n, (p-1)/2, p) == 1:
            s = 1
            q = (p-1)/2
            while True:
                if q % 2 == 0:
                    q = q / 2
                    s += 1
                else:
                    break
            if s == 1:
                r1 = pow(n, (p+1)/4, p)
                r2 = p - r1
                return r1, r2
            else:
                z = 2
                while True:
                    if pow(z, (p-1)/2, p) == p - 1:
                        c = pow(z, q, p)
                        break
                    else:
                        z += 1
                r = pow(n, (q+1)/2, p)
                t = pow(n, q, p)
                m = s
                while True:
                    if t == 1:
                        r1 = r
                        r2 = p - r1
                        return r1, r2
                    else:
                        i = 1
                        while True:
                            if pow(t, 2**i, p) == 1:
                                break
                            else:
                                i += 1
                        b = pow(c, 2**(m-i-1), p)
                        r = r * b % p
                        t = t * b ** 2 % p
                        c = b ** 2 % p
                        m = i
    else:
        return False

def ponc(C, P):
    a, d, p = C
    x, y = P
    return (a*x**2 + y**2 - d*x**2*y**2) % p == 1

def teal(C, P, Q):
    a, d, p = C
    x1, y1 = P
    x2, y2 = Q
    assert ponc(C, P) and ponc(C, Q)
    x3 = (x1 * y2 + y1 * x2) * gmpy.invert(1 + d * x1 * x2 * y1 * y2, p) % p
    y3 = (y1 * y2 - a * x1 * x2) * gmpy.invert(1 - d * x1 * x2 * y1 * y2, p) % p
    return (int(x3), int(y3))

def teml(C, P, l):
    a, d, p = C
    x, y = P
    while l > 1:
        x, y = teal(C, P, P)
        P = (x, y)
        l -= 1
    return P

def encrypt(m, C):
    a, d, p = C
    assert m < 2 * p
    i = 1
    while True:
        r = (a*m**2-1) * gmpy.invert(d*m**2-1, p) % p
        if pow(r, (p-1)/2, p) == 1 and i >= 313 and m < p:
            break
        else:
            m += 2 ** i + 3 * i
            i += 1
    y, _ = tosh(r, p)
    Q = teml(C, (m, y), m % 3)
    return (C, long(Q[1]))

if __name__ == "__main__":
    p = 12961456682267470639726835775555692423332042841451789180700878158315300222996100356887924074868262240805443407987219897961451193726061159305771813188415709L
    C = (3, 2, int(p))

    m1 = 12961456682267470639726835764172752076800558872546236892894593472576943964228308572207806082073733488115041872861195839751739592507375981090427673614632785L
    m2 = 11382940346531483968905552287806251310940919994547754362465959093542738085432239712426493635684589379035469855706750030790881576
    #m = bytes_to_long(flag)
    print encrypt(m2, C)
    print long_to_bytes(m1)
    print long_to_bytes(m2)

    m = 11382940346531483968905552287806251310940919994547754362465959093542738085432239712426493635684589379035469855706750030790881000
    for _ in range(1000):
        print long_to_bytes(m)
        m += 1
