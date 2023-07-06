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
GFmultTable = [[None]]*17
# GFmulTable = [[None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None], [None],
#             [None], [None], [None], [None]]
# GFdivTable=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


def GF_init_logexp_table(m):
    global GFlogTable
    global GFexpTable
    fE = 1
    if GFlogTable[m] != []:
        return
    GFlogTable[m] = np.zeros(fieldSize[m], dtype=int)
    GFexpTable[m] = np.zeros(3*fieldSize[m], dtype=int)
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
    # GFexpTable[m] += fieldOrder[m]
    return

def GF_init_mult_table(m:int):
    global GFmultTable
    global GFlogTable
    global GFexpTable
    if len(GFmultTable[m]) > 1:
        return 0
    GFmultTable[m] = np.zeros((int(fieldSize[m]), int(fieldSize[m])), dtype=int)
    GF_init_logexp_table(m)
    for i in range(1, fieldSize[m]):
        for j in range(1, fieldSize[m]):
            GFmultTable[m][i][j] = GFexpTable[m][GFlogTable[m][i] + GFlogTable[m][j]]
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
    global GFmultTable
    GF_init_mult_table(m)
    mult_table = GFmultTable[m] #[[GF.Multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
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


# def GF_rsgenerator2optG(generator, grsE, m):
#     n = generator.deg + 1
#     vander = np.polynomial.polynomial.polyvander(grsE, n-1)
#     optG = np.zeros((m, n))
#     print(type(generator))
#     for i in range(n):
#         for j in range(m):
#             # print(generator.coeff[i], vander[j][i])
#             optG[j][i] = generator.coeff[i] * vander[j][i]
#
#     return optG


def GF_rsgenerator2optG(optG, generator, grsE, m):
    GF_init_mult_table(m)
    n = optG.shape[1]
    for i in range(n):
        for j in range(i, i + 1 + generator.deg):
            optG[j][i] = GFmultTable[m][generator.coeff[j-i]][grsE[j]]
    return optG


def matrix_opt_mul_A(G, A, start_p:int, m):
    global GFmultTable
    GF_init_mult_table(m)

    tmp1 = np.zeros(G.shape[1], dtype=int)
    tmp2 = np.zeros(G.shape[1], dtype=int)
    tmp3 = np.zeros(G.shape[1], dtype=int)
    tmp4 = np.zeros(G.shape[1], dtype=int)

    if GFMULTAB == 1:
        for j in range(len(A)):
            for i in range(G.shape[1]):
                tmp1[i] = GFmultTable[m][G[start_p+2*j][i]][A[j][0][0]]
                tmp2[i] = GFmultTable[m][G[start_p+2*j][i]][A[j][0][1]]
                tmp3[i] = GFmultTable[m][G[start_p+2*j+1][i]][A[j][1][0]]
                tmp4[i] = GFmultTable[m][G[start_p+2*j+1][i]][A[j][1][1]]
            G[(start_p + 2 * j),:] = GF_addvec(tmp1, tmp3, G[(start_p + 2 * j),:])
            G[(start_p + 2 * j + 1),:] = GF_addvec(tmp2, tmp4, G[(start_p + 2 * j + 1),:])
        print()
        # print(G[-3:])
        # print(G[G!=0])
        #
        # print(len(G[G != 0]), len(G))
        # print('\n\n')
        # for i in range(50):
        #     for j in range(G.shape[1]):
        #         print(G[i][j], end=' ')
        #     print('\n')
        # print('\n\n')
        # print(tmp1)
        # print('\n\n')
        # print(tmp2)
        # print(len(tmp1), G.shape)
        # print(G[start_p+2*0+1][5], A[0][1][1])
        # raise Exception('sodifj')
        return G
    # Not implemented
    return None

def matrix_mul_A(G, A, startP:int, m):
    if G.shape[1] - startP != 2*len(A):
        return None
    mat = np.zeros((G.shape[0], G.shape[1]), dtype=int)
    for i in range(G.shape[0]):
        mat[i: i+startP] = G[i: i+startP]
    for j in range(len(A)):
        for i in range(G.shape[0]):
            b1 = GF_mul(G[i][startP+2*j], A[j][0][0], m)
            b2 = GF_mul(G[i][startP+2*j], A[j][0][1], m)
            b3 = GF_mul(G[i][startP+2*j+1], A[j][1][0], m)
            b4 = GF_mul(G[i][startP+2*j+1], A[j][1][1], m)
            mat[i][startP+2*j] = b1 ^ b3
            mat[i][startP+2*j+1] = b2 ^ b4
    return mat
# def GF_addvec(vec1, vec2, vec3=None):
#     vecSize = len(vec1)
#     longsize = np.dtype(np.uint64).itemsize
#
#     if vec3 is None:
#         vec3 = vec2
#
#     size = (vecSize * np.dtype(np.uint8).itemsize) // longsize
#     longvec1 = np.frombuffer(vec1, dtype=np.uint64)[:size]
#     longvec2 = np.frombuffer(vec2, dtype=np.uint64)[:size]
#     longvec3 = np.frombuffer(vec3, dtype=np.uint64)[:size]
#
#     longvec3 ^= longvec2 ^ longvec1
#
#     for i in range((longsize * size) // np.dtype(np.uint8).itemsize, vecSize):
#         print(type(vec2[i]), type(vec1[i]))
#         vec3[i] = vec2[i] ^ vec1[i]
#
#     return vec3


def GF_addvec(vec1, vec2, vec3=None, vecSize=-1):
    # Czy to jest dobrze? Kto to wie?
    # vecSize = len(vec1)
    if vecSize == -1:
        vecSize = len(vec1)
    if vec3 is None:
        vec3 = vec2
    else:
        vecSize = len(vec3)
    for i in range(vecSize):
        vec3[i] = np.bitwise_xor(vec1[i], vec2[i])
    return vec3

def GF_vecdiv(x, vec, dest, dsize, m):
    global GFlogTable
    global GFexpTable
    global GFmultTable
    GF_init_mult_table(m)
    # mult_table = GFmultTable[m] #[[GF.Multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    if dest == None:
        dest = vec
    if GFMULTAB == 1:
        # print(m, len(fieldOrder), x, len(GFlogTable[m]))
        xinverse = GFexpTable[m][fieldOrder[m] - GFlogTable[m][x]]
        for i in range(dsize):
            # print(xinverse)
            # print(vec[i])
            dest[i] = GFmultTable[m][int(xinverse)][int(vec[i])]
        return dest
    print('GFMULTAB /= 1 NOT IMPLEMENTED')
    return None


def GF_mulvec(x, vec, dest, dsize, m):
    # GF = ffield.FField(m)
    global GFmultTable
    GF_init_mult_table(m)
    # for i in range(50):
    #     for j in range(50):
    #         print(GFmultTable[m][889][j], end=' ')
    #     print()
    # raise Exception('oapsidfj')

    # mult_table = GFmultTable[m]
    # mult_table = [[GF.Multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    if dest is None:
        dest = [0] * dsize #np.zeros(dsize, dtype=int)
    if GFMULTAB == 1:
        for i in range(dsize):
            # print(x, vec[i], GFmultTable[m][x][vec[i]])
            dest[i] = GFmultTable[m][x][vec[i]]
        return dest
    print('GFMULTAB /= 1 NOT IMPLEMENTED')
    return None

def GF_mul(x, y, m):
    # mult_table = [[GF.Multiply(i, j) for j in range(np.power(2, m))] for i in range(np.power(2, m))]
    global GFmultTable
    GF_init_mult_table(m)
    return GFmultTable[m][x][y]

def matrix_echelon(G, m):
    # for i in range(4):
    #     print('===============', i)
    #     for g in G[i]:
    #         print(g, end=' ')
    #     print('\n\n')
    print('\n\n', G.shape, '\n\n')
    n = min(G.shape[0], G.shape[1])
    tmprow = np.zeros(G.shape[1], dtype=int)

    for j in range(n):
        print(j)
        if G[j][j] == 0:
            temp = j
            while (temp < G.shape[0]) and (G[temp][j] == 0):
                temp += 1

            if temp ==  n:
                raise Exception('pasoidfj')
                return None
            tmp = np.copy(G[temp, :])
            G[temp, :] = np.copy(G[j, :])
            G[j, :] = tmp

        G[j, j:] = GF_vecdiv(G[j, j], G[j, j:], None, G.shape[1]-j, m)

        ctr = 0
        for i in range(n):
            if i != j:
                c = G[i][j]
                if c != 0:
                    ctr += 1
                    tmprow = GF_mulvec(c, G[j, j:], tmprow, G.shape[1]-j, m)


                    G[i, j:] = GF_addvec(tmprow, G[i, j:], vecSize=G.shape[1]-j)

    return G


