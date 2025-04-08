from enum import Enum

from ChordProgression import *

class EvaluationResult(Enum):
    EXACT = 1
    CORRECT = 2
    WRONG_EXT = 3
    WRONG_CHORDS = 4
    WRONG_LENGTH = 5

class Game:
    def __init__(self, possible_progs, hard_mode: bool = False):
        self.possible_progs = possible_progs
        self.current_prog = None
        self.current_prog_unique = None
        self.last_guessed_prog = None
        self.last_prog_unique = None
        self.key = Note("C")
        self.hard_mode = hard_mode
        self.next_round()

    def next_round(self):
        self.last_prog_unique = self.current_prog_unique
        self.current_prog = ChordProgression.from_string(random.choice(self.possible_progs))
        self.current_prog_unique = self.current_prog.make_unique(self.key)
        self.last_guessed_prog = None

    def evaluate_guess(self, guess: ChordProgression) -> EvaluationResult:
        if ((self.hard_mode and guess == self.current_prog) or
                (not self.hard_mode and guess.degree_equal(self.current_prog))):
            # Success
            if not self.hard_mode:
                if guess == self.current_prog:
                    return EvaluationResult.EXACT
                else:
                    return EvaluationResult.WRONG_EXT
            else:
                return EvaluationResult.CORRECT
        else:
            # Wrong
            self.last_guessed_prog = guess
            if (len(guess)) != len(self.current_prog):
                return EvaluationResult.WRONG_LENGTH
            else:
                return EvaluationResult.WRONG_CHORDS

    def get_current_prog(self) -> ChordProgression:
        return self.current_prog

    def get_current_prog_unique(self) -> list[UniqueChord]:
        return self.current_prog_unique

    def get_last_guessed_prog(self):
        return self.last_guessed_prog

    def get_last_guessed_prog_unique(self):
        return self.last_guessed_prog.make_unique(self.key)

    def get_last_prog_unique(self):
        return self.last_prog_unique