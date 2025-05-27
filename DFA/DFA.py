#accepta toate sirurile care contin cel putin o aparitie a substringului 011
class DFA:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_state = self.start_state

    def load_config(self, filename):
        with open(filename) as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        config = {}
        transitions_start = False
        self.transitions = {}

        for line in lines:
            if transitions_start:
                parts = line.split()
                if len(parts) != 3:
                    continue
                state, symbol, next_state = parts
                self.transitions[(state, symbol)] = next_state
            else:
                if line == "transitions:":
                    transitions_start = True
                else:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()

        self.states = config['states'].split(',')
        self.alphabet = config['alphabet'].split(',')
        self.start_state = config['start']
        self.accept_states = config['accept'].split(',')

    def reset(self):
        self.current_state = self.start_state

    def process(self, input_str):
        self.reset()
        for ch in input_str:
            if ch not in self.alphabet:
                return False
            key = (self.current_state, ch)
            if key not in self.transitions:
                return False
            self.current_state = self.transitions[key]
        return self.current_state in self.accept_states

if __name__ == "__main__":
    dfa = DFA("dfa_config.txt")

    test_words = [
        "0",
        "1",
        "011",
        "1011",
        "000",
        "111",
        "0101011",
        "0110",
    ]

    for word in test_words:
        result = dfa.process(word)
        print(f"Input: {word} -> Accepted: {result}")
