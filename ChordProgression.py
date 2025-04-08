from Chord import *
import random

SIMPLE_PROGS = [
    "I IV V vi",
    "I IV vi V",
    "I V IV vi",
    "I V vi IV",
    "I vi IV V",
    "I vi V IV",
    "I IV I V",
]

NORMAL_PROGS = [
    "I iii vi IV",
    "I iii IV V",
    "I iii vi V",
    "I IV ii V",
    "I iii ii V",
    "I vi ii V",
    "I vi ii IV",
    "I vi ii iii",
    "I IV V iii",
    "I V IV iii",
    "I vi ii iii",
    "I IV vi iii"
    "I IV ii vi"
]

MINOR_PROGS = [
    "vi iii IV V"
    "vi iii V IV"
    "vi iii ii V"
    "vi iii ii IV"
]

DOMINANT_PROGS = [
    "I III7 IV V",
    "I III7 IV iv",
    "I iii IV iv",
    "I I7 IV V",
    "I I7 IV iv",
    "I Imaj7 I7 VI V",
    "I VI7 ii V7",
    "I VI7 II7 V",
    "I VI7 V IV",
    "I II7 V iV",
    "I II7 IV V"
    "I III7 vi II V",
    "I III7 IV ii V",
    "I III7 vi ii IV",
    "I III7 vi II7 V7",
    "I III7 VI7 II7 V7",
]

TEST_PROG = [
    "I vi ii iii"
]


class ChordProgression:
    def __init__(self, roman_numerals: list[RomanNumeral]):
        self.roman_numerals = roman_numerals

    def make_unique(self, key: Note) -> list[UniqueChord]:
        return [roman_numeral.to_chord(key).make_unique() for roman_numeral in self.roman_numerals]

    def get_roman_numerals(self):
        return self.roman_numerals

    @staticmethod
    def make_random() -> 'ChordProgression':
        return ChordProgression.from_string(random.choice(SIMPLE_PROGS))

    @staticmethod
    def from_string(string: str) -> 'ChordProgression':
        chords_str = string.split(" ")

        chords = []
        for chord_str in chords_str:
            try:
                chords.append(RomanNumeral(chord_str))
            except KeyError and SyntaxError:
                raise SyntaxError(chord_str)
        return ChordProgression(chords)

    @staticmethod
    def get_prog_diff(ref_prog: 'ChordProgression', guessed_prog: 'ChordProgression') -> str:
        diff = ""
        for ref_chord, guessed_chord in zip(ref_prog.get_roman_numerals(), guessed_prog.get_roman_numerals()):
            if ref_chord == guessed_chord:
                diff += guessed_chord.__str__() + " "
            else:
                diff += "x" * len(guessed_chord.__str__()) + " "
        return diff

    def __len__(self):
        return len(self.roman_numerals)

    def __str__(self):
        string = ""
        for chord in self.roman_numerals:
            string += chord.__str__()
            string += " "
        string = string[:-1]
        return string

    def __eq__(self, other: 'ChordProgression'):
        for self_roman, other_roman in zip(self.get_roman_numerals(), other.get_roman_numerals()):
            if self_roman != other_roman:
                return False
        return True

    def degree_equal(self, other: 'ChordProgression'):
        if len(self.get_roman_numerals()) != len(other.get_roman_numerals()):
            return False
        for self_roman, other_roman in zip(self.get_roman_numerals(), other.get_roman_numerals()):
            if not self_roman.degree_equals(other_roman):
                return False
        return True


