from .config import CRYPTO_PADDING
from .config import DECODINGMETHOD
import hashlib
from .objects_def import RlcePrivateKey
from .objects_def import RlcePublicKey
import numpy as np

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
def get_random_bytes_from_command_line(num):
    if num > 64:
        return None
    s = 'Please type at least ' + str(num) + ' characters and then press ENTER\n'
    mes = input(s)
    hash_object = hashlib.sha512()
    hash_object.update(mes.encode(encoding='utf-8'))
    print(hash_object.hexdigest())
    print(len(hash_object.hexdigest()))
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
    print(sk)
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


