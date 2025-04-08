NOTE_TO_FREQ = {}
NOTE_TO_IDX = {
        "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3, "E": 4, "E#": 5, "FB": 4, "F": 5, "F#": 6, "GB": 6,
        "G": 7, "G#": 8, "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11, "B#": 0, "CB": 11,
}

NOTE_IDX_TO_NAME = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A",  "Bb", "B"]
DEGREE_IDX_TO_NAME = ["1", "b2", "2", "b3", "3", "4", "b5", "5", "b6", "6", "b7", "7"]

SCALE_DEGREE_TO_IDX = {
    "1": 0, "#1": 1, "b2": 1, "2": 2, "#2": 3, "b3": 3, "3": 4, "4": 5, "#4": 6, "b5": 6, "5": 7,
    "#5": 8, "b6": 8, "6": 9, "#6": 10, "b7": 10, "7": 11, "b9": 1, "9": 2, "#9": 3, "b11": 4,
    "11": 5, "#11": 6, "b13": 8, "13": 9, "#13": 10,
}

EXT_TO_SCALE_DEGREES = {
    "maj": ["1", "3", "5"],
    "m": ["1", "b3", "5"],
    "7": ["1", "3", "5", "b7"],
    "maj7": ["1", "3", "5", "7"],
    "min7": ["1", "b3", "5", "b7"],
    "dim": ["1", "b3", "b5"],
    "dim7": ["1", "b3", "b5", "6"],
    "min7b5": ["1", "b3", "b5", "b7"],
    "aug": ["1", "3", "#5"],
    "6": ["1", "3", "5", "6"],
    "min6": ["1", "b3", "5", "6"]
}

ROMAN_TO_SCALE_DEGREE = {
    "I": 0, "#I": 1, "BII": 1, "II": 2, "#II": 3, "BIII": 3, "III": 4, "IV": 5, "#IV": 6,
    "BV": 6, "V": 7, "#V": 8, "BVI": 8, "VI": 9, "#VI": 10, "BVII": 10, "VII": 11
}

SCALE_DEGREE_TO_ROMAN = ["I", "bII", "II", "bIII", "III", "IV", "bV", "V", "bVI", "VI", "bVII", "VII"]

JUST_INTONATION_RATIOS = [1/1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8]
def compute_frequencies():
    for octave in range(7):
        for note_name in NOTE_TO_IDX.keys():
            NOTE_TO_FREQ[f"{note_name}{octave}"] = get_frequency(note_name, octave)

def get_frequency(note, octave):

    note_index = NOTE_TO_IDX[note]

    # Calculate semitone distance from A4 (A4 is index 9 in octave 4)
    n = (octave - 4) * 12 + (note_index - 9)

    # Compute frequency
    frequency = 440 * (2 ** (n / 12))
    return frequency

def compute_just_intonation_frequencies():
    for octave in range(7):
        for note_name in NOTE_TO_IDX.keys():
            NOTE_TO_FREQ[f"{note_name}{octave}"] = get_just_intonation_frequency(note_name, octave)

def get_just_intonation_frequency(note_name, octave):
    c4_freq = 261.625565  # Hz
    c4_octave = 4

    if note_name not in NOTE_TO_IDX:
        raise ValueError(f"Invalid note: {note_name}")

    note_idx = NOTE_TO_IDX[note_name]

    c_freq = c4_freq * (2 ** (octave - c4_octave))
    frequency = c_freq * JUST_INTONATION_RATIOS[note_idx]

    return frequency

