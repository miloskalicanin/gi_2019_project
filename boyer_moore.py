heuristics = set([])
pattern = ""


def add_heuristic(heuristic):
    heuristics.add(heuristic)


def set_heuristics(_heuristics):
    global heuristics
    heuristics = _heuristics[:]


def preprocess(_pattern, alphabet=None):
    global pattern
    pattern = _pattern
    [heuristic.preprocess(_pattern, alphabet) for heuristic in heuristics]


def get_offset_matched(**kwargs):
    return max([heuristic.get_offset_matched(**kwargs) for heuristic in heuristics])


def get_offset_mismatched(**kwargs):
    return max([heuristic.get_offset_mismatched(**kwargs) for heuristic in heuristics])


def boyer_moore(text):
    """ Do Boyer-Moore matching """
    i = 0
    occurrences = []
    cnt = 0
    while i < len(text) - len(pattern) + 1:
        shift = 1
        mismatched = False
        for j in range(len(pattern) - 1, -1, -1):
            cnt += 1
            if pattern[j] != text[i + j]:
                shift = max(shift, get_offset_mismatched(mismatch_offset=j,
                                                         current_character=text[i + j],
                                                         first_aligned_character=text[i + len(pattern) - 1],
                                                         next_to_first_aligned_character=text[i + len(pattern) if (
                                                                     i + len(pattern) < len(text)) else -1]))
                mismatched = True
                break
        if not mismatched:
            occurrences.append(i)
            shift = max(shift, get_offset_matched(first_aligned_character=text[i + len(pattern) - 1],
                                                  next_to_first_aligned_character=text[i + len(pattern)
                                                  if (i + len(pattern) < len(text))
                                                  else -1]))
        i += shift
    return occurrences
