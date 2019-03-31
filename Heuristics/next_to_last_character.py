class NextToLastCharacter:
    def __init__(self):
        self._bad_char_tab = {}
        self._pattern_len = 0

    def preprocess(self, pattern, alphabet=None):
        self._bad_char_tab = {}
        for i in range(len(pattern)):
            self._bad_char_tab[pattern[i]] = len(pattern) - i - 1

        self._pattern_len = len(pattern)

    def get_offset_matched(self, **kwargs):
        next_to_last_character = kwargs['next_to_first_aligned_character']
        if next_to_last_character == -1:
            return 0

        return self._bad_char_tab.get(next_to_last_character, self._pattern_len) + 1

    def get_offset_mismatched(self, **kwargs):
        next_to_last_character = kwargs['next_to_first_aligned_character']
        if next_to_last_character == -1:
            return 0

        return self._bad_char_tab.get(next_to_last_character, self._pattern_len) + 1

    def get_name(self):
        return "Next to last character"
