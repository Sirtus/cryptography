from .config import CRYPTO_PADDING
from .config import DECODINGMETHOD
from .config import DRBG
import hashlib
from .objects_def import RlcePrivateKey
from .objects_def import RlcePublicKey
from .objects_def import HashDrbgState
import numpy as np
import random
from .drgb import drbgstate_init
from .byte_functions_lib import random_bytes_2_fe
from .byte_functions_lib import get_permutation
from .byte_functions_lib import permutation_inv
from pyfinite import ffield
from .galois_field import GF_vecinverse


para = {
    'n': 0,
    'k': 0,
    'w': 0,
    'GF_size': 0,
    'hash_type': 0,
    'm_len': 0,  # for medium encoding
    'k1': 0,  # for medium encoding
    'k2': 0,  # for medium encoding
    'k3': 0,  # for medium encoding
    'padding': 0,
    'scheme': 0,
    't': 0,
    'omega': 0,  # for list decoding
    'l_omega': 0,  # for list decoding
    'kappa': 0,
    'u': 0,  # for un-recovered msg symbols by RS
    'cphr_len': 0,  # cipher len in bytes
    'sk_bytes': 0,  # sk bytes for decodingalgorithm 0,1
    'pk_bytes': 0,
    'rand_in_bytes': 0
}


# private
def rlce_private_key_init():
    global para
    key = RlcePrivateKey(para=para, perm1=np.zeros(para['n']),
                         perm2=np.zeros(para['n'] + para['w']),
                         A=np.zeros((para['w'], 2, 2)),
                         grs=np.zeros(para['n']),
                         G=np.zeros((para['k'], para['n'] + para['w'] - para['k'])))
    return key


# private
def rlce_public_key_init():
    global para
    key = RlcePublicKey(para=para, G=np.zeros((para['k'], para['n'] + para['w'] - para['k'])))
    return key


# private
def get_random_bytes_from_command_line(num):
    if num > 64:
        return None
    s = 'Please type at least ' + str(num) + ' characters and then press ENTER\n'
    mes = input(s)
    hash_object = hashlib.sha512()
    hash_object.update(mes.encode(encoding='utf-8'))
    return hash_object.hexdigest()[0:num]


# public
def rlce_keypair(scheme, filename):
    global para
    ret = get_rlce_parameters(scheme, CRYPTO_PADDING)
    if ret is None:
        return None
    randomness = get_random_bytes_from_command_line(para['rand_in_bytes'])
    if randomness is None:
        return None

    sk = rlce_private_key_init()
    pk = rlce_public_key_init()

    nonce = random.getrandbits(128)


    return 0


# private
def get_rlce_parameters(scheme, padding):
    global para
    para['scheme'] = scheme
    para['padding'] = padding

    if scheme == 0:
        para['n'] = 630
        para['k'] = 470
        para['w'] = 160
        para['GF_size'] = 10
        para['hash_type'] = 2
        para['t'] = 80
        para['omega'] = 0
        para['l_omega'] = 0
        para['kappa'] = 128
        para['u'] = 200
        para['cphr_len'] = 988
        if DECODINGMETHOD != 2:
            para['sk_bytes'] = 310116
        else:
            para['sk_bytes'] = 192029
        para['pk_bytes'] = 188001
        para['rand_in_bytes'] = 32

        if padding == 0:
            para['m_len'] = 5500
            para['k1'] = 171
            para['k2'] = 171
            para['k3'] = 346
        elif padding == 1:
            para['m_len'] = 5500
            para['k1'] = 624
            para['k2'] = 32
            para['k3'] = 32
        elif padding == 2:
            para['m_len'] = 4700
            para['k1'] = 146
            para['k2'] = 146
            para['k3'] = 296
        elif padding == 3:
            para['m_len'] = 4700
            para['k1'] = 524
            para['k2'] = 32
            para['k3'] = 32
        elif padding == 4:
            para['m_len'] = 5869
            para['k1'] = 183
            para['k2'] = 183
            para['k3'] = 368
        elif padding == 5:
            para['m_len'] = 5869
            para['k1'] = 670
            para['k2'] = 32
            para['k3'] = 32
        else:
            return None
    elif scheme == 1:
        para['n'] = 1000
        para['k'] = 764
        para['w'] = 236
        para['GF_size'] = 10
        para['hash_type'] = 2
        para['t'] = 118
        para['omega'] = 0
        para['l_omega'] = 0
        para['kappa'] = 192
        para['u'] = 303
        para['cphr_len'] = 1545
        if DECODINGMETHOD != 2:
            para['sk_bytes'] = 747393
        else:
            para['sk_bytes'] = 457073
        para['pk_bytes'] = 450761
        para['rand_in_bytes'] = 40

        if padding == 0:
            para['m_len'] = 8820
            para['k1'] = 275
            para['k2'] = 275
            para['k3'] = 553
        elif padding == 1:
            para['m_len'] = 8820
            para['k1'] = 1007
            para['k2'] = 48
            para['k3'] = 48
        elif padding == 2:
            para['m_len'] = 7640
            para['k1'] = 238
            para['k2'] = 238
            para['k3'] = 479
        elif padding == 3:
            para['m_len'] = 7640
            para['k1'] = 859
            para['k2'] = 48
            para['k3'] = 48
        elif padding == 4:
            para['m_len'] = 9377
            para['k1'] = 293
            para['k2'] = 293
            para['k3'] = 587
        elif padding == 5:
            para['m_len'] = 9377
            para['k1'] = 1077
            para['k2'] = 48
            para['k3'] = 48
        else:
            return None
    elif scheme == 2:
        para['n'] = 1360
        para['k'] = 800
        para['w'] = 560
        para['GF_size'] = 11
        para['hash_type'] = 2
        para['t'] = 280
        para['omega'] = 0
        para['l_omega'] = 0
        para['kappa'] = 256
        para['u'] = 482
        para['cphr_len'] = 2640
        if DECODINGMETHOD != 2:
            para['sk_bytes'] = 1773271
        else:
            para['sk_bytes'] = 1241971
        para['pk_bytes'] = 1232001
        para['rand_in_bytes'] = 48

        if padding == 0:
            para['m_len'] = 11880
            para['k1'] = 371
            para['k2'] = 371
            para['k3'] = 743
        elif padding == 1:
            para['m_len'] = 11880
            para['k1'] = 1365
            para['k2'] = 60
            para['k3'] = 60
        elif padding == 2:
            para['m_len'] = 8800
            para['k1'] = 275
            para['k2'] = 275
            para['k3'] = 550
        elif padding == 3:
            para['m_len'] = 8800
            para['k1'] = 980
            para['k2'] = 60
            para['k3'] = 60
        elif padding == 4:
            para['m_len'] = 13025
            para['k1'] = 407
            para['k2'] = 407
            para['k3'] = 815
        elif padding == 5:
            para['m_len'] = 13025
            para['k1'] = 1509
            para['k2'] = 60
            para['k3'] = 60
        else:
            return None
    else:
        return None
    return 0


def rlce_key_setup(entropy: list, nonce: int, noncelen: int, pk: RlcePublicKey, sk: RlcePrivateKey):
    ret = 0
    m = sk.para['GF_size']
    n = sk.para['n']
    k = sk.para['k']
    w = sk.para['w']
    t = sk.para['t']
    nplusw = n+w
    nminusw = n-w
    LISTDECODE = 0
    if 2*t > n - k:
        LISTDECODE = 1
    nRE = n + (4 + k) * w + 25
    nRBforRE = (m * nRE) / 8
    if (m * nRE) % 8 > 0:
        nRBforRE += 1
    nRB = nRBforRE + 4 * n + 2 * w
    randomBytes = np.zeros(nRB)
    pers = "PostQuantumCryptoRLCEversion2017"
    perlen = len(pers) - 1
    addS = "GRSbasedPostQuantumENCSchemeRLCE"
    addlen = len(addS) - 1

    if DRBG == 0:
        noncehex = "5e7d69e187577b0433eee8eab9f77731"
        if noncelen == 0:
            nonce = int(noncehex, 16)
            drgb_state = drbgstate_init(sk.para['hash_type'])
            # TODO : finish it

    elif DRBG == 1:
        # Not implemented
        None
    elif DRBG == 2:
        # Not implemented
        None

    randE = random_bytes_2_fe(randomBytes, nRBforRE, nRE, m)
    if randE is None:
        return None
    per1 = get_permutation(n, n-1, randomBytes[nRBforRE:])
    per1inv = permutation_inv(per1)

    sk.perm1 = np.copy(per1inv)

    ##
    done = 0
    unknown_index = np.zeros(k)
    known_index = np.zeros(k)

    while done >= 0:
        error_cleared_number = 0
        index1 = 0
        index2 = 0
        per2 = get_permutation(nplusw, nplusw-1, randomBytes[(nRBforRE+2*n-2+done):])
        if per2 is None:
            return None
        for i in range(k):
            if per2[i] < nminusw:
                known_index[index2] = i
                index2 += 1
                error_cleared_number += 1
            else:
                unknown_index[index1] = i
                index1 += 1
        remdim = k - error_cleared_number
        if remdim <= sk.para[15]:
            per2inv = permutation_inv(per2)
            sk.perm2 = np.copy(per2inv)
            done = -1
        else:
            done += 1

    grsvec = randE.copy()
    sk.grs = GF_vecinverse(grsvec, n, m)
    A = np.zeros(w)
