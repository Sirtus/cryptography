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
