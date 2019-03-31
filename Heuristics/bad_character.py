class BadCharacter:
    def __init__(self):
        self.amap = {}
        self.dense_bad_char_tab = []

    def preprocess(self, pattern, alphabet=None):
        """ Given pattern string and list with ordered alphabet characters, create
            and return a dense bad character table.  Table is indexed by offset
            then by character. """
        self.amap = {}
        for i in range(len(alphabet)):
            self.amap[alphabet[i]] = i
        self.dense_bad_char_tab = []
        nxt = [0] * len(self.amap)

        for i in range(0, len(pattern)):
            c = pattern[i]
            assert c in self.amap
            self.dense_bad_char_tab.append(nxt[:])
            nxt[self.amap[c]] = i + 1

    def get_offset_matched(self, **kwargs):
        return 0

    def get_offset_mismatched(self, **kwargs):
        c = kwargs['current_character']
        i = kwargs['mismatch_offset']
        assert c in self.amap
        ci = self.amap[c]
        assert i > (self.dense_bad_char_tab[i][ci] - 1)
        return i - (self.dense_bad_char_tab[i][ci] - 1)

    def get_name(self):
        return "Bad character"


