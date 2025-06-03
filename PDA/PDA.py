# functie care incarca configuratia unui pda (automat cu stiva) dintr-un fisier
def load_config(filename):
    """ citeste configuratia pda-ului din fisier """
    transitions = {}  # dictionar pentru tranzitii
    start = accept = stack_start = None  # starea initiala, finala si simbolul initial al stivei

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # ignora liniile goale si comentariile
            if not line or line.startswith("#"): 
                continue
            # citeste starea de start
            if line.startswith("start"):
                start = line.split("=")[1].strip()
            # citeste starea de acceptare
            elif line.startswith("accept"):
                accept = line.split("=")[1].strip()
            # citeste simbolul initial al stivei
            elif line.startswith("stack_start"):
                stack_start = line.split("=")[1].strip()
            # citeste o tranzitie
            elif "->" in line:
                left, right = line.split("->")
                left_parts = left.strip().split()
                right_parts = right.strip().split()

                # verifica daca tranzitia are formatul corect
                if len(left_parts) != 3 or len(right_parts) != 2:
                    raise ValueError(f"eroare de format in linia: {line}")

                state, symbol, stack_top = left_parts
                next_state, push = right_parts

                # adauga tranzitia in dictionar
                transitions.setdefault((state, symbol, stack_top), []).append((next_state, push))

    # returneaza configuratia
    return start, accept, stack_start, transitions


# functie recursiva care simuleaza executia unui pda
def pda_sim(state, pos, stack, word, accept, transitions):
    """ simuleaza functionarea pda-ului """
    # daca am ajuns la sfarsitul cuvantului
    if pos == len(word):
        # accepta doar daca suntem in starea finala si stiva este goala
        return state == accept and not stack 

    # simbolul curent din cuvant
    symbol = word[pos] if pos < len(word) else 'ε'
    # varful stivei
    top = stack[-1] if stack else None

    # verifica daca exista o tranzitie valida
    if (state, symbol, top) in transitions:
        for next_state, push in transitions[(state, symbol, top)]:
            # pregateste o noua stiva: scoate varful daca era unul
            new_stack = stack[:-1] if top else stack[:]
            # daca trebuie sa punem ceva pe stiva
            if push != 'ε':
                new_stack.extend(push)
            # apeleaza recursiv pda-ul pentru starea urmatoare
            if pda_sim(next_state, pos + 1, new_stack, word, accept, transitions):
                return True
    return False


# codul care se executa doar daca fisierul este rulat direct
if __name__ == "__main__":
    """ incarca configuratia si testeaza pda-ul """
    # incarca configuratia pda-ului
    start, accept, stack_start, transitions = load_config("pda_config.txt")
    
    # cuvinte de test
    test_inputs = ["ab", "aabb", "aaabbb", "aaaabbbb", "aab", "abb", "ba"]
    
    # testeaza fiecare cuvant si afiseaza rezultatul
    for w in test_inputs:
        accepted = pda_sim(start, 0, [stack_start], w, accept, transitions)
        print(f"Input: {w} -> Accepted: {accepted}")
