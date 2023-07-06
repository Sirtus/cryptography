from .objects_def import HashDrbgState, DrbgInput
import numpy as np
import hashlib
import binascii

def drbgstate_init(shatype: int):
    drgb_state = HashDrbgState()
    drgb_state.hashsize = 0
    drgb_state.shatype = shatype

    if shatype == 0:
        drgb_state.seedlen = 55
        drgb_state.security_strength = 112
        drgb_state.hashsize = 5
    if shatype == 1:
        drgb_state.seedlen = 55
        drgb_state.security_strength = 128
        drgb_state.hashsize = 8
    if shatype == 2:
        drgb_state.seedlen = 111
        drgb_state.security_strength = 256
        drgb_state.hashsize = 8

    drgb_state.pf_flag = 0
    drgb_state.reseed_interval = 1 << 48
    drgb_state.max_B_per_req = 65536
    drgb_state.reseed_counter = 0
    drgb_state.V = np.zeros(drgb_state.seedlen, dtype=int)
    drgb_state.C = np.zeros(drgb_state.seedlen, dtype=int)
    return drgb_state


def big_add(num1, num1len, num2, num2len):
    carry = 0
    d = num1len - num2len
    for i in range(num2len-1, -1, -1):

        carry += num1[i+d] + num2[i]
        num1[i+d] = carry & 0xFF
        carry = carry >> 8
    for i in range(d-1, -1 ,-1):
        if carry == 0:
            return num1
        carry = num1[i] + 1
        num1[i] = carry & 0xFF
        carry = carry >> 8
    return num1


def hash_drbg_generate(drbg_state: HashDrbgState, drbg_input: DrbgInput, returned_bytes, req_no_of_bytes):
    if drbg_state.reseed_counter > drbg_state.reseed_interval:
        raise Exception('drgb')
        return None
    hashsize = drbg_state.hashsize
    # wseed = np.zeros(1 + drbg_state.seedlen + drbg_input.addlen)
    wseed = bytearray(bytes([0x00] * (1 + drbg_state.seedlen + drbg_input.addlen)))
    w = np.zeros(hashsize)
    wbytes = bytearray(bytes([0x00] * 4))
    w512 = np.zeros(hashsize)
    w512bytes = bytearray(bytes([0x00] * (8*hashsize)))
    hash_obj = hashlib.sha512()
    if drbg_input.addlen > 0:
        wseed[0] = 0x02
        wseed[1:] = drbg_state.V + bytearray(drbg_input.additional_input.encode())
        if drbg_state.shatype == 2:
            hash_obj.update(wseed)
            hash_str = hash_obj.hexdigest()[:drbg_state.seedlen + 1 + drbg_input.addlen]
            w512 = binascii.unhexlify(hash_str)
            w512bytes = hash_obj.digest()
            # for i in range(64):
            #     w512bytes[i] = (w512[i//8] >> (56 - (i % 8) * 8)) & 0xFF
            drbg_state.V = big_add(drbg_state.V, drbg_state.seedlen, w512bytes, 8*hashsize)

    if req_no_of_bytes > drbg_state.max_B_per_req:
        return None

    data = drbg_state.V.copy()

    m = 0
    one = bytearray(0x01)
    remained_bytes = 0
    tmp = bytearray(bytes([0x00] * 8*hashsize)) #np.zeros(8*hashsize)

    if drbg_state.shatype == 2:
        m = (req_no_of_bytes // (8*hashsize))
        for i in range(m):
            hash_obj.update(data)
            hash_str = hash_obj.hexdigest()[:drbg_state.seedlen]
            w512 = hash_obj.digest() #binascii.unhexlify(hash_str)
            data = big_add(data, drbg_state.seedlen, one, 1)
            for j in range(64):
                returned_bytes[i*64 + j] = w512[j]# (w512[j//8] >> (56 - (j % 8) * 8)) & 0xFF
                # print((w512[j//8] >> (56 - (j % 8) * 8)))
        remained_bytes = req_no_of_bytes % (8*hashsize)
        if remained_bytes > 0:
            hash_obj.update(data)
            # hash_str = hash_obj.hexdigest()[:drbg_state.seedlen]
            w512 = hash_obj.digest() #binascii.unhexlify(hash_str)
            for i in range(64):
                tmp[i] = w512[i] & 0xFF# (w512[i//8] >> (56 - (i % 8) * 8)) & 0xFF
            # for i in range(remained_bytes)""
            returned_bytes[m*8*hashsize: m*8*hashsize+remained_bytes] = tmp[:remained_bytes]

    hseed = np.zeros(1 + drbg_state.seedlen)
    # h512bytes = np.zeros(8*hashsize)
    h512bytes = bytearray(bytes([0x00] * (8*hashsize)))
    reseedbyte = bytearray(bytes([0x00] * 4))
    reseedbyte[0] = (drbg_state.reseed_counter >> 24) & 0xFF
    reseedbyte[1] = (drbg_state.reseed_counter >> 16) & 0xFF
    reseedbyte[2] = (drbg_state.reseed_counter >> 8) & 0xFF
    reseedbyte[3] = drbg_state.reseed_counter & 0xFF

    hseed[0] = 0x03
    hseed[1:] = drbg_state.V[:]

    if drbg_state.shatype == 2:
        hash_obj.update(hseed)
        hash_str = hash_obj.hexdigest()[:drbg_state.seedlen + 1]
        h512 = hash_obj.digest()#binascii.unhexlify(hash_str)
        for i in range(64):
            h512bytes[i] = (h512[i // 8] >> (56 - (i % 8) * 8)) & 0xFF
        drbg_state.V = big_add(drbg_state.V, drbg_state.seedlen, h512bytes, 8*hashsize)
        drbg_state.V = big_add(drbg_state.V, drbg_state.seedlen, drbg_state.C, drbg_state.seedlen)
        drbg_state.V = big_add(drbg_state.V, drbg_state.seedlen, reseedbyte, 4)
    # for o in returned_bytes:
    #     print(o, end = ' ')
    drbg_state.reseed_counter += 1
    return drbg_state, returned_bytes


def hash_drbg(drbg_state: HashDrbgState, drbg_input: DrbgInput, output):
    ret = 0
    outlen = len(output)
    drbg_state = hash_drbg_instantiate(drbg_state, drbg_input)
    if ret < 0:
        return None
    loop = outlen // drbg_state.max_B_per_req
    rem = outlen % drbg_state.max_B_per_req

    returned_bytes = bytearray(bytes([0x00] * drbg_state.max_B_per_req ))

    for i in range(loop):
        drbg_state, output[i * drbg_state.max_B_per_req:] = hash_drbg_generate(drbg_state, drbg_input, output[i * drbg_state.max_B_per_req:], drbg_state.max_B_per_req)
        if drbg_state is None:
            return None

    if rem > 0:
        drbg_state, returned_bytes = hash_drbg_generate(drbg_state, drbg_input, returned_bytes, rem)
        if drbg_state is None:
            return None
        output[loop*drbg_state.max_B_per_req:loop*drbg_state.max_B_per_req+rem] = returned_bytes[:rem]
    # print('\n\n')
    # for x in output:
    #     print(x, end=' ')
    # print('\n\n')
    return output


def num2str(n):
    n_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    n_bytes_str = ''.join([chr(b) for b in n_bytes])
    return n_bytes_str


def hash_drbg_instantiate(drbg_state: HashDrbgState, drbg_input: DrbgInput):
    seed_material_len = drbg_input.entropylen + drbg_input.noncelen + drbg_input.perslen
    print(hex(ord(drbg_input.entropy[0])))

    seed_material = bytearray(drbg_input.entropy.encode()) + bytearray(drbg_input.nonce.to_bytes(drbg_input.noncelen, 'big')) \
                    + bytearray(drbg_input.personalization_string.encode())  # concatenation of 3 arrays
    print('before: ', drbg_state.V)
    drbg_state.V = drbg_hash_df(drbg_state.shatype, seed_material, seed_material_len, drbg_state.V, drbg_state.seedlen)
    print('after: ', drbg_state.V)
    seedC = bytearray(0x00) + drbg_state.V[:drbg_state.seedlen]
    drbg_state.C = drbg_hash_df(drbg_state.shatype, seedC, drbg_state.seedlen + 1, drbg_state.C, drbg_state.seedlen)
    drbg_state.reseed_counter = 1
    return drbg_state


def drbg_hash_df(shatype, input, inputlen, output, outputlen):
    output = bytearray(bytes([0x00] * outputlen))
    seed = bytearray(bytes([0x00] * 5)) + input
    outputlenbits = 8*outputlen
    seed[4] = (0xFF & outputlenbits)
    seed[3] = (0xFF & (outputlenbits >> 8))
    seed[2] = (0xFF & (outputlenbits >> 16))
    seed[1] = (0xFF & (outputlenbits >> 24))
    seed[0] = (0x01)

    if shatype == 2:
        hashsize = 8
        ctr = 8 * hashsize
        hash_obj = hashlib.sha512()

        for i in range(outputlen):
            hash512 = hash_obj.digest()
            if ctr == 8 * hashsize:
                hash_obj.update(seed)
                hash_str = hash_obj.digest()[:hashsize*8]
                hash512 = hash_obj.digest()
                seed[0] += 1
                ctr = 0
            output[i] = hash512[i%hashsize] #>> (56-(ctr % 8) * 8)) & 0xFF #(hash512[ctr//8] >> (56-(ctr % 8) * 8)) & 0xFF
            ctr += 1
    # for i in output:
    #     print(i, end=' ')
    # print('\n')
    # print('outlen ', outputlen)
    return output

