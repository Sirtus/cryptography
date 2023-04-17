from objects_def import HashDrbgState
import numpy as np

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
    drgb_state.V = np.zeros(drgb_state.seedlen)
    drgb_state.C = np.zeros(drgb_state.seedlen)
    return drgb_state