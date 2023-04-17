class RlcePrivateKey:
    def __init__(self, para=None, perm1=None, perm2=None, generator=None, A=None, S=None, grs=None, G=None):
        self.para = para
        self.perm1 = perm1
        self.perm2 = perm2
        self.generator = generator
        self.A = A
        self.S = S
        self.grs = grs
        self.G = G


class RlcePublicKey:
    def __init__(self, para=None, G=None):
        self.para = para
        self.G = G


class HashDrbgState:
    def __init__(self, seedlen=None, shatype= None, hashsize=None, pf_flag=None, reseed_interval=None,
                 max_B_per_req=None, security_strength=None, reseed_counter=None, V=None, C=None):
        self.seedlen = seedlen
        self.shatype = shatype
        self.hashsize = hashsize
        self.pf_flag = pf_flag
        self.reseed_interval = reseed_interval
        self.max_B_per_req = max_B_per_req
        self.security_strength = security_strength
        self.reseed_counter = reseed_counter
        self.V = V
        self.C = C
