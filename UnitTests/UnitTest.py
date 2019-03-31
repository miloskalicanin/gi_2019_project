import unittest
from utils import get_alphabet
from Heuristics.good_suffix import GoodSuffix
from Heuristics.bad_character import BadCharacter
from Heuristics.last_character import LastCharacter
from Heuristics.next_to_last_character import NextToLastCharacter
from Heuristics.bmhs2 import HorspoolSunday2
import boyer_moore as bm


class TestStringMethods(unittest.TestCase):

    def test_parsing_alphabet(self):
        text = "DABECCDEABCBD"
        alphabet = get_alphabet(text)
        self.assertEqual("ABCDE", alphabet)
        self.assertNotEqual("DABEC", alphabet)
        self.assertNotEqual("DABECCDEABCBD", alphabet)

    def test_boyer_moore(self):
        gs = GoodSuffix()
        bc = BadCharacter()
        lc = LastCharacter()
        nlc = NextToLastCharacter()
        bmhs2 = HorspoolSunday2()

        # test heuristics
        self.assertEqual(set([]), bm.heuristics)
        bm.add_heuristic(gs)
        self.assertEqual({gs}, bm.heuristics)
        bm.add_heuristic(gs)
        self.assertEqual({gs}, bm.heuristics)
        bm.add_heuristic(bc)
        self.assertEqual({gs, bc}, bm.heuristics)
        self.assertNotEqual({gs, bc, lc}, bm.heuristics)
        bm.add_heuristic(lc)
        self.assertEqual({gs, bc, lc}, bm.heuristics)
        bm.add_heuristic(nlc)
        self.assertEqual({gs, bc, lc, nlc}, bm.heuristics)
        bm.add_heuristic(bmhs2)
        self.assertEqual({gs, bc, lc, nlc, bmhs2}, bm.heuristics)

        # test algorithm
        self.assertEqual("", bm.pattern)
        self.assertEqual({}, bc.amap)
        self.assertEqual([], bc.dense_bad_char_tab)
        self.assertEqual("", gs.pattern)
        self.assertEqual([], gs.lp)
        self.assertEqual([], gs.big_l)
        self.assertEqual([], gs.small_l_prime)
        self.assertEqual({}, lc._bad_char_tab)
        self.assertEqual(0, lc._pattern_len)

        input_text = "DEBEAAABCBEADEEABC"
        pattern = "AABCBEAD"
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)

        self.assertEqual({'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}, bc.amap)
        self.assertEqual([[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 3, 0, 0, 0],
                          [2, 3, 4, 0, 0], [2, 5, 4, 0, 0], [2, 5, 4, 0, 6], [7, 5, 4, 0, 6]], bc.dense_bad_char_tab)
        self.assertEqual(0, bc.get_offset_matched())
        self.assertEqual(3, bc.get_offset_mismatched(mismatch_offset=7, current_character=input_text[7]))
        self.assertEqual(2, bc.get_offset_mismatched(mismatch_offset=7, current_character=input_text[10]))

        self.assertEqual(pattern, bm.pattern)
        self.assertEqual({'A': 1, 'B': 3, 'C': 4, 'E': 2}, lc._bad_char_tab)
        self.assertEqual(8, lc._pattern_len)
        self.assertEqual(0, lc.get_offset_matched())
        self.assertEqual(1, lc.get_offset_mismatched(first_aligned_character='A'))
        self.assertEqual(3, lc.get_offset_mismatched(first_aligned_character='B'))
        self.assertEqual(4, lc.get_offset_mismatched(first_aligned_character='C'))
        self.assertEqual(8, lc.get_offset_mismatched(first_aligned_character='D'))
        self.assertEqual(8, lc.get_offset_mismatched(first_aligned_character='Y'))
        self.assertEqual(2, lc.get_offset_mismatched(first_aligned_character='E'))

        self.assertEqual({'A': 1, 'B': 3, 'C': 4, 'D': 0, 'E': 2}, nlc._bad_char_tab)
        self.assertEqual(8, nlc._pattern_len)
        self.assertEqual(0, nlc.get_offset_mismatched(next_to_first_aligned_character=-1))
        self.assertEqual(2, nlc.get_offset_mismatched(next_to_first_aligned_character='A'))
        self.assertEqual(4, nlc.get_offset_mismatched(next_to_first_aligned_character='B'))
        self.assertEqual(5, nlc.get_offset_mismatched(next_to_first_aligned_character='C'))
        self.assertEqual(1, nlc.get_offset_mismatched(next_to_first_aligned_character='D'))
        self.assertEqual(9, nlc.get_offset_mismatched(next_to_first_aligned_character='Y'))
        self.assertEqual(3, nlc.get_offset_mismatched(next_to_first_aligned_character='E'))

        self.assertEqual({'A': 1, 'AA': 6, 'B': 3, 'AB': 5, 'C': 4, 'BC': 4, 'CB': 3, 'E': 2, 'BE': 2, 'EA': 1, 'D': 0, 'AD': 0}, bmhs2._bad_char_tab)
        self.assertEqual(8, bmhs2._pattern_len)

    def test_boyer_moore_results(self):
        gs = GoodSuffix()
        bc = BadCharacter()
        lc = LastCharacter()
        nlc = NextToLastCharacter()
        bmhs2 = HorspoolSunday2()

        input_text = "BCDAAAABBBCBDBCDBAACBDABCDAAAABBBCBDBCDBAACBDCBDCAAAAAAACCCCCACABBACBACBDCBDCBBABBBCBCBCBDACBDCBCBDCBACBACBDCBDCBBABBBCBCBCBDAABAB"
        pattern = "CBDC"
        expected_result = [42, 45, 70, 73, 91, 96, 105, 108]

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(gs)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(bc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(lc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(nlc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(bmhs2)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        pattern = "AABB"
        expected_result = [5, 28]

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(gs)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(bc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(lc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(nlc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(bmhs2)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        input_text = "CCCACCAAABAAACCCCC"
        pattern = "AA"
        expected_result = [6, 7, 10, 11]

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(gs)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(bc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(lc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(nlc)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)

        bm.heuristics = set([])
        bm.pattern = ""
        bm.add_heuristic(bmhs2)
        alphabet = get_alphabet(input_text)
        bm.preprocess(_pattern=pattern, alphabet=alphabet)
        result = bm.boyer_moore(input_text)
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
