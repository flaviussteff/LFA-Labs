# clasa care defineste un nfa (automat finit nedeterminist)
class NFA:
    def __init__(self, config_file):
        # dictionar care va contine tranzitiile nfa-ului
        self.transitions = {}
        # citeste configuratia automatului din fisier
        self.read_config(config_file)

    # functie care citeste configuratia dintr-un fisier
    def read_config(self, filename):
        with open(filename) as f:
            # elimina liniile goale si comentariile
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        # prima linie contine starile, separate prin virgula
        self.states = lines[0].split('=')[1].strip().split(',')
        # a doua linie contine alfabetul (simbolurile)
        self.alphabet = lines[1].split('=')[1].strip().split(',')
        # a treia linie contine starea de start
        self.start_state = lines[2].split('=')[1].strip()
        # a patra linie contine starile de acceptare
        self.accept_states = lines[3].split('=')[1].strip().split(',')

        # gaseste indexul de unde incep tranzitiile
        trans_index = lines.index('transitions:')

        # parcurge liniile cu tranzitii
        for line in lines[trans_index + 1:]:
            parts = line.split()
            if len(parts) != 3:
                continue  # ignora liniile invalide
            state, symbol, next_state = parts  # desparte linia in cele 3 componente
            key = (state, symbol)  # cheia este un tuplu (stare curenta, simbol)
            if key not in self.transitions:
                self.transitions[key] = []  # initializeaza lista daca nu exista
            self.transitions[key].append(next_state)  # adauga starea destinatie

    # functie care verifica daca un cuvant este acceptat de nfa
    def accepts(self, word):
        # porneste de la starea initiala
        current_states = [self.start_state]

        # pentru fiecare simbol din cuvant
        for symbol in word:
            next_states = []  # lista starilor urmatoare
            for state in current_states:
                key = (state, symbol)  # formeaza cheia (stare, simbol)
                if key in self.transitions:
                    next_states += self.transitions[key]  # adauga starile urmatoare
            # elimina duplicatele
            current_states = list(set(next_states))

        # verifica daca cel putin una dintre starile finale este atinsa
        return any(state in self.accept_states for state in current_states)


# cod care se executa doar daca fisierul este rulat direct
if __name__ == "__main__":
    # initializeaza nfa-ul cu configuratia din fisier
    nfa = NFA("nfa_config.txt")

    # cuvinte de test pentru verificare
    test_inputs = ["01", "001", "0001", "1", "10", "100", "1101"]

    # testeaza fiecare cuvant si afiseaza rezultatul
    for word in test_inputs:
        result = nfa.accepts(word)
        print(f"Input: {word} -> Accepted: {result}")
