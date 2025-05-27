#nfa care accepta sirurile care se termina in 01
class NFA:
    def __init__(self, config_file):
        self.transitions = {}
        self.read_config(config_file)

    def read_config(self, filename):
        with open(filename) as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        self.states = lines[0].split('=')[1].strip().split(',')
        self.alphabet = lines[1].split('=')[1].strip().split(',')
        self.start_state = lines[2].split('=')[1].strip()
        self.accept_states = lines[3].split('=')[1].strip().split(',')

        trans_index = lines.index('transitions:')
        for line in lines[trans_index + 1:]:
            parts = line.split()
            if len(parts) != 3:
                continue
            state, symbol, next_state = parts
            key = (state, symbol)
            if key not in self.transitions:
                self.transitions[key] = []
            self.transitions[key].append(next_state)

    def accepts(self, word):
        current_states = [self.start_state]

        for symbol in word:
            next_states = []
            for state in current_states:
                key = (state, symbol)
                if key in self.transitions:
                    next_states += self.transitions[key]
            current_states = list(set(next_states))

        return any(state in self.accept_states for state in current_states)


if __name__ == "__main__":
    nfa = NFA("nfa_config.txt")

    test_inputs = ["01", "001", "0001", "1", "10", "100", "1101"]

    for word in test_inputs:
        result = nfa.accepts(word)
        print(f"Input: {word} -> Accepted: {result}")
