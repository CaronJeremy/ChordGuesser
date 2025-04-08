import numpy as np
import sounddevice as sd
from Chord import *
from Note import *


def play_note(note: UniqueNote, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.25 * np.sin(2 * np.pi * note.get_frequency() * t)
    sd.play(wave, samplerate=sample_rate)
    sd.wait()


def play_chord(chord: UniqueChord, duration=2.0, sample_rate=44100):
    frequencies = chord.get_frequencies()
    print(frequencies)
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = sum(0.25 * np.sin(2 * np.pi * f * t) for f in frequencies)
    wave = wave / max(abs(wave))  # Normalize
    sd.play(wave, samplerate=sample_rate)
    sd.wait()

def play_chord_sequence(unique_chords: list[UniqueChord], duration=1.5, sample_rate=44100):
    full_wave = np.array([])

    for unique_chord in unique_chords:
        frequencies = unique_chord.get_frequencies()
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = sum(0.5 * np.sin(2 * np.pi * f * t) for f in frequencies)
        wave = wave / max(abs(wave))  # Normalize
        full_wave = np.concatenate((full_wave, wave))

    sd.play(full_wave, samplerate=sample_rate)
    sd.wait()