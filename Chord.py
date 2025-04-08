import random

from Note import *

class Chord:
    def __init__(self, notes: set[Note]):
        self.notes = notes

    @classmethod
    def from_degrees(cls, degrees: set[Degree], root: Note) -> 'Chord':
        return Chord({degree.to_note(root) for degree in degrees})

    @classmethod
    def from_name(cls, name: str) -> 'Chord':
        if len(name) > 1 and (name[1] == "#" or name[1].lower() == "b"):
            root = name[0:2]
            extension = name[2:]
        else:
            root = name[0]
            extension = name[1:]
        if extension == "":
            extension = "maj"
        try:
            degrees = {Degree(degree) for degree in EXT_TO_SCALE_DEGREES[extension.lower()]}
        except KeyError:
            raise KeyError("This chord name isn't valid")
        return Chord.from_degrees(degrees, Note(root))

    def make_unique(self) -> 'UniqueChord':
        return UniqueChord({note.make_unique(random.choice([3, 4])) for note in self.notes})

    def get_notes(self) -> set[Note]:
        return self.notes

    # handles chord + chord or chord + note
    def __add__(self, other):
        if isinstance(other, Note):  # Add a Note to an existing Chord
            return Chord(self.notes | {other})
        elif isinstance(other, Chord):  # Merge two chords
            return Chord(self.notes | other.get_notes())
        raise TypeError("Can only add Note or Chord")

    # for doing note + chord
    def __radd__(self, other: Note):
        if isinstance(other, Note):
            return Chord(self.notes | {other})
        raise TypeError("Can only add Note or Chord")

    def __str__(self) -> str:
        out = ""
        for note in self.notes:
            out += note.__str__() + " "
        return out


class UniqueChord:
    def __init__(self, unique_notes: set[UniqueNote]):
        self.unique_notes = unique_notes

    @classmethod
    def from_note_names(cls, unique_note_names: set[str]) -> 'UniqueChord':
        return UniqueChord({UniqueNote.from_name(unique_note_name) for unique_note_name in unique_note_names})

    def get_unique_notes(self) -> set[UniqueNote]:
        return self.unique_notes

    def get_frequencies(self) -> set[float]:
        return {unique_note.get_frequency() for unique_note in self.unique_notes}

    def make_non_unique(self) -> Chord:
        notes = set()
        for unique_note in self.unique_notes:
            notes.add(unique_note.get_note())
        return Chord(notes)

    def __add__(self, other):
        if isinstance(other, UniqueNote):
            return UniqueChord(self.unique_notes | {other})
        elif isinstance(other, UniqueChord):
            return UniqueChord(self.unique_notes | other.get_unique_notes())
        raise TypeError("Can only add Unique Note or Unique Chord")

    def __radd__(self, other: UniqueNote):
        if isinstance(other, UniqueNote):
            return UniqueChord(self.unique_notes | {other})
        raise TypeError("Can only add Unique Note or Unique Chord")

    def __str__(self) -> str:
        out = ""
        for unique_note in self.unique_notes:
            out += unique_note.__str__() + " "
        return out

class ChordDegree:
    def __init__(self, degrees: set[Degree]):
        self.degrees = degrees

    @staticmethod
    def from_string(roman_numeral: str) -> 'ChordDegree':
        return RomanNumeral(roman_numeral).to_chord_degree()

    def get_degrees(self) -> set[Degree]:
        return self.degrees

    def to_chord(self, root: Note) -> Chord:
        return Chord({degree.to_note(root) for degree in self.degrees})

    def __add__(self, other):
        if isinstance(other, Degree):
            return ChordDegree(self.degrees | {other})
        elif isinstance(other, ChordDegree):
            return ChordDegree(self.degrees | other.get_degrees())
        raise TypeError("Can only add Degree or ChordDegree")

    def __radd__(self, other: Degree):
        if isinstance(other, Degree):
            return ChordDegree(self.degrees | {other})
        raise TypeError("Can only add Degree or ChordDegree")

    def __str__(self) -> str:
        string = ""
        for degree in self.degrees:
            string += f"{degree} "
        return string

    def __eq__(self, other: 'ChordDegree') -> bool:
        for self_degree, other_degree in zip(self.degrees, other.get_degrees()):
            if self_degree != other_degree:
                return False
        return True

class RomanNumeral:
    def __init__(self, roman_numeral: str):
        self.root_degree = self.get_root_degree(roman_numeral)
        self.ext = self.extract_ext(roman_numeral)

    def get_root_degree_idx(self):
        return self.root_degree

    def get_ext(self):
        return self.ext

    def to_chord_degree(self) -> ChordDegree:
        return ChordDegree(self.get_degrees())

    def to_chord(self, scale_root: Note) -> Chord:
        return Chord({degree.to_note(scale_root) for degree in self.get_degrees()})

    def get_degrees(self) -> set[Degree]:
        degrees_string = EXT_TO_SCALE_DEGREES[self.ext]
        ext_degrees = {Degree(degree_string) for degree_string in degrees_string}
        return {degree.with_different_root_degree(self.root_degree) for degree in ext_degrees}

    def degree_equals(self, other: 'RomanNumeral') -> bool:
        return self.get_root_degree_idx() == other.get_root_degree_idx()

    def __eq__(self, other: 'RomanNumeral') -> bool:
        return self.get_degrees() == other.get_degrees()

    def __str__(self):
        roman_str = SCALE_DEGREE_TO_ROMAN[self.root_degree.get_idx()]
        if self.ext == "maj":
            return roman_str
        elif self.ext == "m":
            return roman_str.lower()
        return roman_str+self.ext

    @staticmethod
    def get_root_degree(roman_numeral: str) -> Degree:
        return Degree(ROMAN_TO_SCALE_DEGREE[RomanNumeral.remove_ext(roman_numeral).upper()])

    @staticmethod
    def remove_ext(roman_str: str) -> str:
        roman_str_copy = roman_str
        while roman_str.upper() not in ROMAN_TO_SCALE_DEGREE.keys():
            roman_str = roman_str[:-1]
            if len(roman_str) == 0:
                raise SyntaxError(f"Invalid roman numeral: {roman_str_copy}")
        return roman_str

    @staticmethod
    def extract_ext(roman_str: str) -> str:
        roman_str_copy = roman_str
        if roman_str.upper() in ROMAN_TO_SCALE_DEGREE.keys():
            if roman_str[0].lower() == "b" or roman_str[0] == "#":
                roman_str = roman_str[1:]
            if roman_str.isupper():
                return "maj"
            elif roman_str.islower():
                return "m"
            else:
                raise SyntaxError(f"Ambiguous chord type`{roman_str_copy}")

        while roman_str.lower() not in EXT_TO_SCALE_DEGREES.keys():
            roman_str = roman_str[1:]
            if len(roman_str) == 0:
                raise SyntaxError(f"Invalid chord extension: {roman_str_copy}")
        return roman_str.lower()
