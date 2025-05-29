def load_config(filename):
    """ Citeste configuratia PDA-ului din fisier. """
    transitions = {}
    start = accept = stack_start = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): 
                continue
            if line.startswith("start"):
                start = line.split("=")[1].strip()
            elif line.startswith("accept"):
                accept = line.split("=")[1].strip()
            elif line.startswith("stack_start"):
                stack_start = line.split("=")[1].strip()
            elif "->" in line:
                left, right = line.split("->")
                left_parts = left.strip().split()
                right_parts = right.strip().split()

                if len(left_parts) != 3 or len(right_parts) != 2:
                    raise ValueError(f"Eroare de format in linia: {line}")

                state, symbol, stack_top = left_parts
                next_state, push = right_parts

                transitions.setdefault((state, symbol, stack_top), []).append((next_state, push))

    return start, accept, stack_start, transitions

def pda_sim(state, pos, stack, word, accept, transitions):
    """ Simuleaza functionarea PDA-ului. """
    if pos == len(word):
        return state == accept and not stack 

    symbol = word[pos] if pos < len(word) else 'ε'
    top = stack[-1] if stack else None

    if (state, symbol, top) in transitions:
        for next_state, push in transitions[(state, symbol, top)]:
            new_stack = stack[:-1] if top else stack[:]
            if push != 'ε':
                new_stack.extend(push)
            if pda_sim(next_state, pos + 1, new_stack, word, accept, transitions):
                return True
    return False

if __name__ == "__main__":
    """ Incarca configuratia si testeaza PDA-ul. """
    start, accept, stack_start, transitions = load_config("pda_config.txt")
    test_inputs = ["ab", "aabb", "aaabbb", "aaaabbbb", "aab", "abb", "ba"]
    
    for w in test_inputs:
        accepted = pda_sim(start, 0, [stack_start], w, accept, transitions)
        print(f"Input: {w} -> Accepted: {accepted}")
