#a^n * b^n
def load_config(filename):
    transitions = {}
    start = accept = stack_start = None
    with open(filename) as f:
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
                state, symbol, stack_top = left.strip().split()
                next_state, push = right.strip().split()
                transitions.setdefault((state, symbol, stack_top), []).append((next_state, push))
    return start, accept, stack_start, transitions

def pda_sim(state, pos, stack, word, accept, transitions, depth=0, max_depth=1000):
    if depth > max_depth:
        return False
    if pos > len(word):
        return False

    # Dacă suntem în starea accept și am consumat tot inputul
    if state == accept and pos == len(word):
        return True

    symbol = word[pos] if pos < len(word) else 'ε'
    top = stack[-1] if stack else None

    # Explorează toate tranzițiile posibile
    for (s, sym, stk_top), outcomes in transitions.items():
        if s != state:
            continue
        if sym != symbol and sym != 'ε':
            continue
        if stk_top != top:
            continue
        for next_state, push in outcomes:
            new_stack = stack[:-1] if stk_top else list(stack)
            if push != 'ε':
                for c in reversed(push):
                    new_stack.append(c)
            next_pos = pos + (0 if sym == 'ε' else 1)
            if pda_sim(next_state, next_pos, new_stack, word, accept, transitions, depth+1, max_depth):
                return True
    return False

if __name__ == "__main__":
    start, accept, stack_start, transitions = load_config("pda_config.txt")
    test_inputs = ["", "ab", "aabb", "aaabbb", "aab", "abb", "ba", "aaaabbb"]
    for w in test_inputs:
        accepted = pda_sim(start, 0, [stack_start], w, accept, transitions)
        print(f"Input: {w} -> Accepted: {accepted}")
