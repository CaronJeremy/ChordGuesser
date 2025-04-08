# note: A note in a scale. Ex: Bb, C, F
# unique_note: A note and its octave. Ex: A4, F#3
# EXT: the extension of a chord. Ex: min, aug, dim7 (major is notated as "maj" instead of nothing)
# Scale_degree: note degree relative to the root. Ex: 1, b3, 5, #9, #b13
# note_idx: index of a note. Ex: C=1, C#=2, Db=2, D=3, etc.
from ChordUtil import *

class Note:
    def __init__(self, note_name_or_idx):
        if isinstance(note_name_or_idx, str):
            self.note_idx = NOTE_TO_IDX[note_name_or_idx.upper()]
        elif isinstance(note_name_or_idx, int):
            self.note_idx = note_name_or_idx
        else:
            raise TypeError("Use note name or note index")

    def make_unique(self, octave: int) -> 'UniqueNote':
        return UniqueNote(self, octave)

    def get_idx(self) -> int:
        return self.note_idx

    @staticmethod
    def from_degree(degree: 'Degree', root: 'Note') -> 'Note':
        return Note((degree.get_idx() + root.get_idx()) % 12)

    def __add__(self, other: 'Note'):
        from Chord import Chord
        if isinstance(other, Note):
            return Chord({self, other})  # Create a Chord with both notes
        raise TypeError("Can only add Note to another Note")

    def __eq__(self, other: "Note"):
        return self.note_idx == other.note_idx

    def __hash__(self):
        return hash(self.note_idx)

    def __str__(self) -> str:
        return NOTE_IDX_TO_NAME[self.note_idx]

class Degree:
    def __init__(self, degree_name_or_idx):
        if isinstance(degree_name_or_idx, str):
            self.degree_idx = SCALE_DEGREE_TO_IDX[degree_name_or_idx.lower()]
        elif isinstance(degree_name_or_idx, int):
            self.degree_idx = degree_name_or_idx % 12
        else:
            raise TypeError("Use degree name or note index")

    def to_note(self, root: Note) -> Note:
        return Note.from_degree(self, root)

    def with_different_root_degree(self, root_degree: 'Degree'):
        return Degree((self.degree_idx + root_degree.degree_idx) % 12)

    def get_idx(self) -> int:
        return self.degree_idx

    def __eq__(self, other: "Degree"):
        return self.degree_idx == other.degree_idx

    def __hash__(self):
        return hash(self.degree_idx)

    def __str__(self) -> str:
        return DEGREE_IDX_TO_NAME[self.degree_idx]

class UniqueNote:
    def __init__(self, note: Note, octave: int):
        self.note = note
        self.octave = octave

    @classmethod
    def from_name(cls, unique_note_name: str) -> 'UniqueNote':
        octave = int(unique_note_name[-1])
        if len(unique_note_name) == 2:
            note_name = unique_note_name[0]
        elif len(unique_note_name) == 3:
            note_name = unique_note_name[0:2]
        else:
            raise SyntaxError("Not a valid note, forgot to specify the octave?")
        note = Note(note_name)

        return UniqueNote(note, octave)

    def get_note(self) -> Note:
        return self.note

    def get_octave(self) -> int:
        return self.octave

    def get_frequency(self) -> float:
        return NOTE_TO_FREQ[self.__str__().upper()]

    def __eq__(self, other: "UniqueNote"):
        return self.note == other.note and self.octave == other.octave

    def __hash__(self):
        return hash((self.note, self.octave))

    def __add__(self, other):
        from Chord import UniqueChord
        if isinstance(other, UniqueNote):
            return UniqueChord({self, other})
        raise TypeError("Can only add unique note to another unique note or chord")

    def __str__(self) -> str:
        return f"{self.note}{self.octave}"
