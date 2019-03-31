class LastCharacter:
    def __init__(self):
        self._bad_char_tab = {}
        self._pattern_len = 0

    def preprocess(self, pattern, alphabet=None):
        self._bad_char_tab = {}
        for i in range(len(pattern) - 1):
            self._bad_char_tab[pattern[i]] = len(pattern) - i - 1

        self._pattern_len = len(pattern)


    def get_offset_matched(self, **kwargs):
        return 0

    def get_offset_mismatched(self, **kwargs):
        c = kwargs['first_aligned_character']

        return self._bad_char_tab.get(c, self._pattern_len)

    def get_name(self):
        return "Last character"
