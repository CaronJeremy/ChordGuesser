from ChordPlayer import *
from Game import *
class ChordGuesser:
    def __init__(self, possible_progs, hard_mode: bool):
        self.possible_progs = possible_progs
        self.current_prog = None
        self.last_guessed_prog = None
        self.last_prog = None
        self.key = Note("C")
        self.hard_mode = hard_mode

    def play(self):
        print("Type \"help\" for help")
        self.progression_create()
        self.progression_ask_guess()
        while True:
            user_in = input()
            keep_going = self.parse_keyword(user_in)
            if keep_going:
                self.evaluate_answer(user_in)

    # return: Keep going? True: yes, False: no
    def parse_keyword(self, keyword) -> bool:
        keyword = keyword.lower()
        if keyword in ["quit", "stop", "exit", "q"]:
            quit()
        elif keyword in ["help", "h"]:
            print(""" The following keywords are available:
            quit: quit the game
            help: this
            again: hear the progression again
            skip: skip this progression
            hear guess: plays the last guessed progression
            previous: hear the previous progression
            """)
            return False
        elif keyword in ["again", "a"]:
            self.progression_play(self.current_prog)
            return False
        elif keyword in ["skip", "s"]:
            print("Skipping this progression")
            print("The answer was " + self.current_prog.__str__())
            self.progression_create()
            self.progression_ask_guess()
            return False
        elif keyword in ["hear guess", "hg"]:
            if self.last_guessed_prog is not None:
                self.progression_play(self.last_guessed_prog)
            else:
                print("No valid progressions have been entered yet")
            return False
        elif keyword in ["previous", "p", "hear last", "hl"]:
            if self.last_prog is not None:
                self.progression_play(self.last_prog)
            else:
                print("This is the first progression")
            return False
        return True

    def progression_create(self):
        self.last_prog = self.current_prog
        self.current_prog = ChordProgression.from_string(random.choice(self.possible_progs))
        self.last_guessed_prog = None

    def progression_ask_guess(self):
        print("Guess the chord progression!")
        self.progression_play(self.current_prog)

    def progression_play(self, progression: ChordProgression):
        play_chord_sequence(progression.make_unique(self.key))

    def evaluate_answer(self, user_in: str):
        try:
            guess = ChordProgression.from_string(user_in)
        except SyntaxError:
            print("Invalid guess, wrong syntax and not a keyword")
            return
        if ((self.hard_mode and guess == self.current_prog) or
                (not self.hard_mode and guess.degree_equal(self.current_prog))):
            if not self.hard_mode:
                if guess == self.current_prog:
                    print("Congrats! That was the exact progression")
                else:
                    print("Congrats! The right extensions were " + self.current_prog.__str__())
            else:
                print("Congrats!")
            self.progression_create()
            self.progression_ask_guess()
        else:
            self.last_guessed_prog = guess
            if (len(guess)) != len(self.current_prog):
                print(f"Wrong amount of chord in guessed progression. \n"
                      f"Answer has {len(self.current_prog)} chords but your guess had {len(guess)}")
            else:
                print('Wrong, guess again. (type "again" to hear again)')
                print(ChordProgression.get_prog_diff(self.current_prog, guess))
            self.progression_play(self.current_prog)


if __name__ == '__main__':
    compute_frequencies()
    ALL_PROGS = SIMPLE_PROGS + NORMAL_PROGS + MINOR_PROGS + DOMINANT_PROGS
    game = ChordGuesser(ALL_PROGS, False)
    game.play()
    # print(play_chord_sequence(cpf.make_chord_sequence("I", "Imaj7", "I7", "IV", "iv")))

