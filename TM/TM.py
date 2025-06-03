class turingmachine:
    def __init__(self, config_file):
        # dictionar pentru tranzitii
        self.states = {}
        # stare curenta initiala
        self.current_state = 'q0'
        # banda sub forma de lista de caractere
        self.tape = []
        # pozitia capului de citire pe banda
        self.head_position = 0
        # incarcam configuratia din fisier
        self.load_config(config_file)
    
    def load_config(self, config_file):
        # citeste fisierul config si populeaza tranzitiile
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                # ignoram liniile goale sau comentarii
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    # fiecare tranzitie are 5 parti: stare, simbol citit, simbol scris, directie, stare urmatoare
                    if len(parts) == 5:
                        state, read_char, write_char, move, next_state = parts
                        # daca starea nu exista in dictionar, o cream
                        if state not in self.states:
                            self.states[state] = {}
                        # adaugam tranzitia pentru starea si simbolul citit
                        self.states[state][read_char] = (write_char, move, next_state)
    
    def set_tape(self, input_string):
        # seteaza banda initiala cu sirul de intrare (lista de caractere)
        self.tape = list(input_string)
        # pozitia capului de citire porneste de la 0
        self.head_position = 0
    
    def get_current_char(self):
        # obtine simbolul curent sub capul de citire
        # daca capul este in afara benzii, returneaza simbol blank '_'
        if self.head_position < 0 or self.head_position >= len(self.tape):
            return '_'
        return self.tape[self.head_position]
    
    def write_char(self, char):
        # scrie simbolul pe banda la pozitia capului
        # daca pozitia depaseste lungimea benzii, extinde banda cu blank-uri
        while len(self.tape) <= self.head_position:
            self.tape.append('_')
        # daca pozitia este negativa, inseram la inceput si mutam capul la 0
        if self.head_position < 0:
            self.tape.insert(0, char)
            self.head_position = 0
        else:
            self.tape[self.head_position] = char
    
    def move_head(self, direction):
        # muta capul de citire la stanga sau dreapta
        if direction == 'R':
            self.head_position += 1
        elif direction == 'L':
            self.head_position -= 1
    
    def run(self, max_steps=1000):
        # executa masina turing pana la max_steps sau pana cand se ajunge in starea 'HALT'
        step = 0
        while step < max_steps and self.current_state != 'HALT':
            current_char = self.get_current_char()
            
            # afisam pasul curent, starea, pozitia capului si caracterul citit
            print(f"pas {step}: stare={self.current_state}, pozitie={self.head_position}, caracter='{current_char}'")
            print(f"banda: {''.join(self.tape)}")
            print()
            
            # daca avem tranzitie definita pentru starea si simbolul citit
            if self.current_state in self.states and current_char in self.states[self.current_state]:
                write_char, move, next_state = self.states[self.current_state][current_char]
                
                # scriem simbolul pe banda
                self.write_char(write_char)
                # mutam capul in directia specificata
                self.move_head(move)
                # schimbam starea
                self.current_state = next_state
            else:
                # daca nu exista tranzitie pentru starea si simbolul curent, oprim executia
                print(f"tranzitie nedefinita pentru starea {self.current_state} si caracterul '{current_char}'")
                break
            
            step += 1
        
        # afisam banda finala
        print(f"rezultat final: {''.join(self.tape)}")
        return ''.join(self.tape)

# exemplu de folosire
if __name__ == "__main__":
    # cream masina turing cu configuratia din fisier
    tm = turingmachine('config.txt')
    
    # setam banda initiala: sirul de copiat + simbol $ + # + spatiu pentru copie + #
    test_input = "10011$#_______#"
    tm.set_tape(test_input)
    
    print("=== masina turing - copiere sir ===")
    print(f"input: {test_input}")
    print("=" * 40)
    
    # rulam masina
    result = tm.run()
