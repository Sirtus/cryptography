import numpy as np
from pyfinite import ffield
import numpy as np
from .config import GFMULTAB
import struct

fieldOrder= [0, 0, 0, 0, 0, 0, 0, 0, (1<<8)-1, (1<<9)-1, (1<<10)-1, (1<<11)-1, (1<<12)-1, (1<<13)-1,
             (1<<14)-1, (1<<15)-1, (1<<16)-1]
fieldSize=[0,0,0,0,0,0,0,0,(1<<8), (1<<9),(1<<10),(1<<11),(1<<12),(1<<13),(1<<14),(1<<15),(1<<16)]
poly = [0,0,0,0,0,0,0,0,0x0163,0x0211,0x0409,0x0805,0x1099,0x2129,0x5803,0x8003,0x002D]
GFlogTable = [np.array([])]*17
GFexpTable = [np.array([])]*17

# GFmulTable = [[None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None],
#             [None], [None], [None], [None]]
# GFdivTable=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


def GF_init_logexp_table(m):
    global GFlogTable
    global GFexpTable
    fE = 1
    if GFlogTable[m] != []:
        return
    GFlogTable[m] = np.zeros(fieldSize[m], dtype=np.int8)
    GFexpTable[m] = np.zeros(3*fieldSize[m], dtype=np.int8)
    for j in range(fieldSize[m]):
        GFlogTable[m][j] = fieldOrder[m]

    GFexpTable[m][0] = 1
    GFexpTable[m][fieldSize[m]] = 1

    for j in range(fieldOrder[m]):
        GFlogTable[m][fE] = j
        GFexpTable[m][j] = fE
        fE = fE << 1
        if fE & fieldSize[m]:
            fE = (fE ^ poly[m]) & (fieldOrder[m])
    GFexpTable[m][fieldOrder[m]:2*fieldOrder[m]] = GFexpTable[m][:fieldOrder[m]]
    GFexpTable[m][2*fieldOrder[m]:3*fieldOrder[m]] = GFexpTable[m][:fieldOrder[m]]
    GFexpTable[m] += fieldOrder[m]
    return


def GF_vecinverse(vec1, vecsize, m):
    GF = ffield.FField(m)
    global GFlogTable
    global GFexpTable
    GF_init_logexp_table(m)
    vec2 = [GFexpTable[m][fieldOrder[m] - GFlogTable[m][vec1[i]]] for i in range(vecsize)]
    return vec2


def getMatrixAandAinv(mat, matInv, randomElements, randBytes, m):
    GF = ffield.FField(m)
    global GFlogTable
    global GFexpTable
    GF_init_logexp_table(m)
    mult_table = [[GF.Multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    randB = 0
    j = 0
    # for i in randomElements:
    #     print(i, end = ' ')
    # raise Exception("aposidfjsdpaoifjsdpofij")
    for i in range(randBytes):
        if randomElements[i] != 0:
            randomElements[randB] = randomElements[i]
            randB += 1
    if GFMULTAB == 1:
        for i in range(len(mat)):
            det = 0
            while det == 0:
                a = mult_table[randomElements[j]][randomElements[j+3]]
                det = a ^ mult_table[randomElements[j+1]][randomElements[j+2]]
                if det == 0:
                    j += 1
                if j+4 > randB:
                    return None, None

            mat[i][0][0] = randomElements[j]
            mat[i][0][1] = randomElements[j+1]
            mat[i][1][0] = randomElements[j+2]
            mat[i][1][1] = randomElements[j+3]
            a = GFexpTable[m][fieldOrder[m] - GFlogTable[m][det]]
            matInv[i][0][0] = mult_table[randomElements[j + 3]][a]
            matInv[i][1][0] = mult_table[randomElements[j + 2]][a]
            j += 4
        return mat, matInv

    # not implemented
    return None, None


def GF_rsgenerator2optG(generator, grsE, m):
    n = generator.deg + 1
    vander = np.polynomial.polynomial.polyvander(grsE, n-1)
    optG = np.zeros((m, n))
    print(type(generator))
    for i in range(n):
        for j in range(m):
            optG[j][i] = generator.coeff[i] * vander[j][i]

    return optG


def matrix_opt_mul_A(G, A, start_p, m):
    GF = ffield.FField(m)
    mult_table = [[GF.multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    tmp1 = tmp2 = tmp3 = tmp4 = np.zeros(G.shape[1])
    if GFMULTAB == 1:
        for j in range(len(A)):
            for i in range(G.shape[1]):
                tmp1[i] = mult_table[G[start_p+2*j][i]][A[j][0][0]]
                tmp2[i] = mult_table[G[start_p+2*j][i]][A[j][0][1]]
                tmp3[i] = mult_table[G[start_p+2*j+1][i]][A[j][1][0]]
                tmp4[i] = mult_table[G[start_p+2*j+1][i]][A[j][1][1]]
            G[(start_p + 2 * j):] = GF_addvec(tmp1, tmp3, G[(start_p + 2 * j):])
            G[(start_p + 2 * j + 1):] = GF_addvec(tmp2, tmp4, G[(start_p + 2 * j + 1):])
        return G
    # Not implemented
    return None

def GF_addvec(vec1, vec2, vec3=None):
    vecSize = len(vec1)
    longsize = np.dtype(np.uint64).itemsize

    if vec3 is None:
        vec3 = vec2

    size = (vecSize * np.dtype(np.uint8).itemsize) // longsize
    longvec1 = np.frombuffer(vec1, dtype=np.uint64)[:size]
    longvec2 = np.frombuffer(vec2, dtype=np.uint64)[:size]
    longvec3 = np.frombuffer(vec3, dtype=np.uint64)[:size]

    longvec3 ^= longvec2 ^ longvec1

    for i in range((longsize * size) // np.dtype(np.uint8).itemsize, vecSize):
        vec3[i] = vec2[i] ^ vec1[i]

    return vec3


def GF_vecdiv(x, vec, dest, dsize, m):
    GF = ffield.FField(m)
    global GFlogTable
    global GFexpTable
    GF_init_logexp_table(m)
    mult_table = [[GF.multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    if dest == None:
        dest = vec
    if GFMULTAB == 1:
        xinverse = GFexpTable[fieldOrder[m] - GFlogTable[x]]
        for i in range(dsize):
            dest[i] = mult_table[xinverse][vec[i]]
        return dest
    print('GFMULTAB /= 1 NOT IMPLEMENTED')
    return None


def GF_mulvec(x, vec, dest, dsize, m):
    GF = ffield.FField(m)
    mult_table = [[GF.multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    if dest == None:
        dest = vec
    if GFMULTAB == 1:
        for i in range(dsize):
            dest[i] = mult_table[x][vec[i]]
        return dest
    print('GFMULTAB /= 1 NOT IMPLEMENTED')
    return None

def matrix_echelon(G, m):
    n = min(G.shape[0], G.shape[1])
    tmprow = np.zeros(G.shape[1])
    for j in range(n):
        if G[j][j] == 0:
            temp = j
            while ((temp < G.shape[0]) and (G[temp][j] == 0)):
                temp += 1
            if temp ==  n:
                return None
            G[j], G[temp] = G[temp], G[j]
        G[j:, j:] = GF_vecdiv(G[j, j], G[j:, j:], None, G.shape[1]-1, m)
        for i in range(n):
            if i != j:
                c = G[i][j]
                if c != 0:
                    tmprow = GF_mulvec(c, G[j:, j:], tmprow, G.shape[1]-j, m)
                    G[j:, j:] = GF_addvec(tmprow, G[j:, j:])
    return G


