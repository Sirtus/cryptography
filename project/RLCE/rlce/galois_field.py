import numpy as np
from pyfinite import ffield

fieldOrder= [0, 0, 0, 0, 0, 0, 0, 0, (1<<8)-1, (1<<9)-1, (1<<10)-1, (1<<11)-1, (1<<12)-1, (1<<13)-1,
             (1<<14)-1, (1<<15)-1, (1<<16)-1]
fieldSize=[0,0,0,0,0,0,0,0,(1<<8), (1<<9),(1<<10),(1<<11),(1<<12),(1<<13),(1<<14),(1<<15),(1<<16)]
poly = [0,0,0,0,0,0,0,0,0x0163,0x0211,0x0409,0x0805,0x1099,0x2129,0x5803,0x8003,0x002D]

GFlogTable=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
GFexpTable=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
GFmulTable=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
GFdivTable=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


def GF_vecinverse(vec1, vecsize, m):
    GF = ffield.FField(m)
    log_table = GF.logarithm_table()
    exp_table = GF.exponent_table()
    vec2 = [exp_table[GF.modulus - log_table[vec1[i]]] for i in range(vecsize)]
    return vec2



def GF_init_logexp_table(m):
    j = 1
    fE = 1
    if GFlogTable[m] is not None:
        return 0
    GFlogTable[m] = np.zeros(fieldSize[m])
    if GFlogTable[m] is None:
        return None
    GFexpTable[m] = np.zeros(3*fieldSize[m])
    if GFexpTable is None:
        return None
    for j in range(fieldSize[m]):
        GFlogTable[m][j] = fieldOrder[m]
    GFexpTable[m][0] = 1
    GFexpTable[m][fieldOrder[m]] = 1
    for j in range(fieldOrder[m]):
        GFlogTable[m][fE] = j
        GFexpTable[m][j] = fE
        fE = fE << 1
        if fE & fieldSize[m]:
            fE = (fE ^ poly[m]) & fieldOrder[m]
    GFexpTable[m][fieldOrder[m]]