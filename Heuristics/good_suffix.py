class GoodSuffix:
    def __init__(self):
        self.pattern = ""
        self.lp = []
        self.big_l = []
        self.small_l_prime = []

    def __z_array(self, s):
        """ Use Z algorithm (Gusfield theorem 1.4.1) to preprocess s """
        assert len(s) > 1
        z = [len(s)] + [0] * (len(s) - 1)
        # Initial comparison of s[1:] with prefix
        for i in range(1, len(s)):
            if s[i] == s[i - 1]:
                z[1] += 1
            else:
                break
        r, l = 0, 0
        if z[1] > 0:
            r, l = z[1], 1
        for k in range(2, len(s)):
            assert z[k] == 0
            if k > r:
                # Case 1
                for i in range(k, len(s)):
                    if s[i] == s[i - k]:
                        z[k] += 1
                    else:
                        break
                r, l = k + z[k] - 1, k
            else:
                # Case 2
                # Calculate length of beta
                nbeta = r - k + 1
                zkp = z[k - l]
                if nbeta > zkp:
                    # Case 2a: Zkp wins
                    z[k] = zkp
                else:
                    # Case 2b: Compare characters just past r
                    nmatch = 0
                    for i in range(r + 1, len(s)):
                        if s[i] == s[i - k]:
                            nmatch += 1
                        else:
                            break
                    l, r = k, r + nmatch
                    z[k] = r - k + 1
        return z

    def __n_array(self, s):
        """ Compile the N array (Gusfield theorem 2.2.2) from the Z array """
        return self.__z_array(s[::-1])[::-1]

    def __big_l_prime_array(self, p, n):
        """ Compile L' array (Gusfield theorem 2.2.2) using p and N array.
            L'[i] = largest index j less than n such that N[j] = |P[i:]| """
        lp = [0] * len(p)
        for j in range(len(p) - 1):
            i = len(p) - n[j]
            if i < len(p):
                lp[i] = j + 1
        return lp

    def __big_l_array(self, p, lp):
        """ Compile L array (Gusfield theorem 2.2.2) using p and L' array.
            L[i] = largest index j less than n such that N[j] >= |P[i:]| """
        l = [0] * len(p)
        l[1] = lp[1]
        for i in range(2, len(p)):
            l[i] = max(l[i - 1], lp[i])
        return l

    def __small_l_prime_array(self, n):
        """ Compile lp' array (Gusfield theorem 2.2.4) using N array. """
        small_lp = [0] * len(n)
        for i in range(len(n)):
            if n[i] == i + 1:  # prefix matching a suffix
                small_lp[len(n) - i - 1] = i + 1
        for i in range(len(n) - 2, -1, -1):  # "smear" them out to the left
            if small_lp[i] == 0:
                small_lp[i] = small_lp[i + 1]
        return small_lp

    def preprocess(self, pattern, alphabet=None):
        """ Return tables needed to apply good suffix rule. """
        self.pattern = pattern
        n = self.__n_array(pattern)
        self.lp = self.__big_l_prime_array(pattern, n)
        self.big_l = self.__big_l_array(pattern, self.lp)
        self.small_l_prime = self.__small_l_prime_array(n)

    def get_offset_matched(self, **kwargs):
        """ Given a full match of P to T, return amount to shift as
            determined by good suffix rule. """
        return len(self.small_l_prime) - self.small_l_prime[1]

    def get_offset_mismatched(self, **kwargs):
        """ Given a mismatch at offset i, and given L/L' and l' arrays,
            return amount to shift as determined by good suffix rule. """
        i = kwargs['mismatch_offset']
        length = len(self.big_l)
        assert i < length
        if i == length - 1:
            return 0
        i += 1  # i points to leftmost matching position of P
        if self.big_l[i] > 0:
            return length - self.big_l[i]
        return length - self.small_l_prime[i]

    def get_name(self):
        return "Good suffix"
