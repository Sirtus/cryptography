import numpy as np
import random


def random_bytes_2_fe(random_bytes, nRB, output_size, m):
    vec = np.zeros(output_size)
    if m == 8:
        for i in range(nRB):
            vec[i] = random_bytes[i]
    elif m == 9:
        vec = b2fe9(random_bytes, nRB, len(vec))
    elif m == 10:
        vec = b2fe10(random_bytes, nRB, len(vec))
    elif m == 11:
        vec = b2fe11(random_bytes, nRB, len(vec))
    elif m == 12:
        vec = b2fe12(random_bytes, nRB, len(vec))

    return vec


def b2fe9(byts, blen, size):
    if 9*size > 8*blen:
        return None
    bits = 0x00
    used = 0
    fe = np.zeros(size)
    j = 0
    for i in range(size):
        if used == 0:
            fe[i] = byts[j]
            fe[i] = fe[i] << 1
            j += 1
            bits = (byts[j] & 0x80)
            fe[i] = fe[i] | bits
            used = 1

        elif used == 1:
            fe[i] = (byts[j] << 1) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xC0
            bits = bits >> 6
            fe[i] = fe[i] | bits
            used = 2

        elif used == 2:
            fe[i] = (byts[j] << 2) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xE0
            bits = bits >> 5
            fe[i] = fe[i] | bits
            used = 3
        elif used == 3:
            fe[i] = (byts[j] << 3) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xF0
            bits = bits >> 4
            fe[i] = fe[i] | bits
            used = 4
        elif used == 4:
            fe[i] = (byts[j] << 4) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xF8
            bits = bits >> 3
            fe[i] = fe[i] | bits
            used = 5
        elif used == 5:
            fe[i] = (byts[j] << 5) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xFC
            bits = bits >> 2
            fe[i] = fe[i] | bits
            used = 6
        elif used == 6:
            fe[i] = (byts[j] << 6) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xFE
            bits = bits >> 1
            fe[i] = fe[i] | bits
            used = 7
        elif used == 7:
            fe[i] = (byts[j] << 7) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xFF
            bits = bits >> 6
            fe[i] = fe[i] | bits
            j += 1
            used = 0

        else:
            return None

    return fe


def b2fe10(byts, blen, size):
    if 10*size > 8*blen:
        return None
    byts = byts.astype(int)
    bits = 0x00
    used = 0
    fe = np.zeros(size, dtype=np.int32)
    j = 0
    for i in range(size):
        if used == 0:
            fe[i] = byts[j]
            fe[i] = fe[i] << 2
            j += 1
            bits = (byts[j] & 0xC0)
            bits = bits >> 6
            fe[i] = fe[i] | bits
            used = 2

        elif used == 2:
            fe[i] = (byts[j] << 2) & 0x00FF
            fe[i] = fe[i] << 2
            j += 1
            bits = byts[j] & 0xF0
            bits = bits >> 4
            fe[i] = fe[i] | bits
            used = 4

        elif used == 4:
            fe[i] = (byts[j] << 4) & 0x00FF
            fe[i] = fe[i] << 2
            j += 1
            bits = byts[j] & 0xFC
            bits = bits >> 2
            fe[i] = fe[i] | bits
            used = 6

        elif used == 6:
            fe[i] = (byts[j] << 6) & 0x00FF
            fe[i] = fe[i] << 2
            j += 1
            bits = byts[j] & 0xFF
            bits = bits >> 1
            fe[i] = fe[i] | bits
            j += 1
            used = 0

        else:
            return None

    return fe


def b2fe11(byts, blen, size):
    if 11*size > 8*blen:
        return None
    bits = 0x00
    used = 0
    fe = np.zeros(size)
    j = 0
    for i in range(size):
        if used == 0:
            fe[i] = byts[j]
            fe[i] = fe[i] << 3
            j += 1
            bits = (byts[j] & 0xE0)
            bits = bits >> 5
            fe[i] = fe[i] | bits
            used = 3

        elif used == 3:
            fe[i] = (byts[j] << 3) & 0x00FF
            fe[i] = fe[i] << 3
            j += 1
            bits = byts[j] & 0xFC
            bits = bits >> 2
            fe[i] = fe[i] | bits
            used = 6

        elif used == 6:
            fe[i] = (byts[j] << 6) & 0x00FF
            fe[i] = fe[i] << 2
            j += 1
            bits = byts[j] & 0xFF
            fe[i] = fe[i] | bits
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0x80
            bits = bits >> 7
            fe[i] = fe[i] | bits
            used = 1

        elif used == 1:
            fe[i] = (byts[j] << 1) & 0x00FF
            fe[i] = fe[i] << 3
            j += 1
            bits = byts[j] & 0xF0
            bits = bits >> 4
            fe[i] = fe[i] | bits
            used = 4

        elif used == 4:
            fe[i] = (byts[j] << 4) & 0x00FF
            fe[i] = fe[i] << 3
            j += 1
            bits = byts[j] & 0xFE
            bits = bits >> 1
            fe[i] = fe[i] | bits
            used = 7

        elif used == 7:
            fe[i] = (byts[j] << 7) & 0x00FF
            fe[i] = fe[i] << 1
            j += 1
            bits = byts[j] & 0xFF
            fe[i] = fe[i] | bits
            fe[i] = fe[i] << 2
            j += 1
            bits = byts[j] & 0xC0
            bits = bits >> 6
            fe[i] = fe[i] | bits
            used = 2

        elif used == 2:
            fe[i] = (byts[j] << 2) & 0x00FF
            fe[i] = fe[i] << 3
            j += 1
            bits = byts[j] & 0xF8
            bits = bits >> 3
            fe[i] = fe[i] | bits
            used = 5

        elif used == 5:
            fe[i] = (byts[j] << 5) & 0x00FF
            fe[i] = fe[i] << 3
            j += 1
            bits = byts[j] & 0xFF
            fe[i] = fe[i] | bits
            j += 1
            used = 0

        else:
            return None

    return fe


def b2fe12(byts, blen, size):
    if 12*size > 8*blen:
        return None
    bits = 0x00
    used = 0
    fe = np.zeros(size)
    j = 0
    for i in range(size):
        if used == 0:
            fe[i] = byts[j]
            fe[i] = fe[i] << 4
            j += 1
            bits = (byts[j] & 0xF0)
            bits = bits >> 4
            fe[i] = fe[i] | bits
            used = 4

        elif used == 4:
            fe[i] = (byts[j] << 4) & 0x00FF
            fe[i] = fe[i] << 4
            j += 1
            fe[i] = fe[i] | byts[j]
            j += 1
            used = 0

        else:
            return None

    return fe


def get_permutation(persize, t, randbytes):
    permutation = np.zeros(persize)
    for i in range(persize):
        permutation[i] = i
    random_short_integers = getShortIntegers(randbytes, t)
    for i in range(t):
        swapi = random_short_integers[i] % (persize - i)
        swapi += i
        permutation[i], permutation[swapi] = permutation[swapi], permutation[i]
    return permutation


def getShortIntegers(randb, outsize):
    out = np.zeros(outsize, dtype=int)
    randb = randb.astype(int)
    for i in range(outsize):
        out[i] = randb[2*i]
        out[i] = (out[i] << 8) & 0xFFFF
        out[i] = out[i] | randb[2*i+1]
        out[i] = out[i] & 0xFFFF
    return out


def permutation_inv(p):
    p = p.astype(int)
    result = np.zeros(len(p))
    for i in range(len(p)):
        result[p[i]] = i
    return result

