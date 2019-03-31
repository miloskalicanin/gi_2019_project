class HorspoolSunday2:
    def __init__(self):
        self._bad_char_tab = {}
        self._pattern_len = 0
        self._first_character_ = ""

    def preprocess(self, pattern, alphabet=None):
        self._bad_char_tab = {}
        for i in range(len(pattern)):
            self._bad_char_tab[pattern[i]] = len(pattern) - i - 1
            if i != 0:
                self._bad_char_tab[pattern[i - 1] + pattern[i]] = len(pattern) - i - 1

        self._first_character_ = pattern[0]
        self._pattern_len = len(pattern)

    def get_offset_matched(self, **kwargs):
        last_character = kwargs['first_aligned_character']
        next_to_last_character = kwargs['next_to_first_aligned_character']
        if next_to_last_character == -1:
            return 0

        offset_next_to_last_character = self._bad_char_tab.get(next_to_last_character, self._pattern_len) + 1

        if offset_next_to_last_character == self._pattern_len or offset_next_to_last_character == self._pattern_len + 1:
            return offset_next_to_last_character

        offset_last_character = self._bad_char_tab.get(last_character + next_to_last_character, self._pattern_len) + 1

        if offset_last_character == self._pattern_len + 1 and next_to_last_character == self._first_character_:
            return self._pattern_len

        return offset_last_character

    def get_offset_mismatched(self, **kwargs):
        last_character = kwargs['first_aligned_character']
        next_to_last_character = kwargs['next_to_first_aligned_character']
        if next_to_last_character == -1:
            return 0

        offset_next_to_last_character = self._bad_char_tab.get(next_to_last_character, self._pattern_len) + 1

        if offset_next_to_last_character == self._pattern_len or offset_next_to_last_character == self._pattern_len + 1:
            return offset_next_to_last_character

        offset_last_character = self._bad_char_tab.get(last_character + next_to_last_character, self._pattern_len) + 1

        if offset_last_character == self._pattern_len + 1 and next_to_last_character == self._first_character_:
            return self._pattern_len

        return offset_last_character

    def get_name(self):
        return "Horspool Sunday 2"
