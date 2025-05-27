class TuringMachine:
    def __init__(self, config_file, tape_file):
        self.load_config(config_file)
        self.load_tape(tape_file)
        self.head = 0
        self.state = self.start_state

    def load_config(self, filename):
        with open(filename) as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        def get_line_starting_with(prefix):
            for line in lines:
                if line.startswith(prefix):
                    return line[len(prefix):].strip()
            return ''

        self.states = get_line_starting_with('states:').split(',')
        self.tape_alphabet = get_line_starting_with('tape_alphabet:').split(',')
        self.blank = get_line_starting_with('blank:')
        self.start_state = get_line_starting_with('start_state:')
        self.accept_states = get_line_starting_with('accept_states:').split(',')

        self.transitions = {}
        trans_index = lines.index('transitions:') + 1
        for line in lines[trans_index:]:
            if '->' not in line:
                continue
            left, right = line.split('->')
            left = left.strip()
            right = right.strip()
            curr_state, read_sym = left.split()
            next_state, write_sym, direction = right.split()
            self.transitions[(curr_state, read_sym)] = (next_state, write_sym, direction)

    def load_tape(self, tape_file):
        with open(tape_file) as f:
            tape_str = f.readline().strip()
            self.tape = list(tape_str)

    def step(self):
        if self.head < 0:
            self.tape.insert(0, self.blank)
            self.head = 0
        if self.head >= len(self.tape):
            self.tape.append(self.blank)

        curr_sym = self.tape[self.head]
        key = (self.state, curr_sym)
        if key not in self.transitions:
            return False

        next_state, write_sym, direction = self.transitions[key]
        self.tape[self.head] = write_sym
        self.state = next_state

        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1
        elif direction == 'S':
            pass
        else:
            raise Exception(f"Directie necunoscuta: {direction}")

        return True

    def run(self, max_steps=10000):
        steps = 0
        while self.state not in self.accept_states and steps < max_steps:
            if not self.step():
                break
            steps += 1
        return ''.join(self.tape), self.state in self.accept_states

if __name__ == "__main__":
    tm = TuringMachine("tm_config.txt", "tape.txt")
    final_tape, accepted = tm.run()
    print("Final tape:", final_tape)
    print("Accepted:", accepted)