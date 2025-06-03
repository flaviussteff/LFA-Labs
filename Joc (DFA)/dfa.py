# functie care incarca configuratia unui dfa dintr-un fisier text
def parse_config(path):
    # citeste liniile din fisier, eliminand comentariile si liniile goale
    with open(path, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    # initializeaza structura de configurare
    config = {
        'zones': {},         # dictionar cu zonele (starile) si tranzitiile acestora
        'alphabet': [],      # alfabetul admis (comenzile posibile)
        'start': '',         # zona de start
        'accept': set(),     # multimea zonelor de acceptare (finale)
        'links': []          # camp neutilizat, dar prezent in structura
    }

    current_section = None  # retine sectiunea curenta din fisier

    # parcurge fiecare linie pentru a construi configuratia
    for line in lines:
        if line.startswith("states:"):
            current_section = 'states'  # incepe sectiunea starilor
            zone_names = line.split(":")[1].split()  # extrage numele starilor
            for name in zone_names:
                config['zones'][name] = {}  # initializeaza dictionar gol pentru fiecare stare
        elif line.startswith("alphabet:"):
            config['alphabet'] = line.split(":")[1].split()  # extrage alfabetul (lista de comenzi)
        elif line.startswith("start:"):
            config['start'] = line.split(":")[1].strip()  # extrage zona de start
        elif line.startswith("accept:"):
            config['accept'] = set(line.split(":")[1].split())  # extrage zonele finale
        elif line.startswith("transitions:"):
            current_section = 'transitions'  # incepe sectiunea tranzitiilor
        elif current_section == 'transitions':
            src, symbol, dst = line.split()  # extrage tranzitia: sursa, simbol, destinatie
            config['zones'][src][symbol] = dst  # seteaza tranzitia in structura

    return config  # returneaza configuratia completa


# functie care simuleaza o secventa de comenzi pe baza configuratiei
def simulate_path(config, path):
    # seteaza zona curenta la cea de start
    location = config['start']
    actions = path.strip().split()  # imparte secventa in comenzi individuale

    print(f"\nincepi misiunea din zona: {location}")

    # parcurge fiecare comanda introdusa
    for step in actions:
        if step not in config['alphabet']:
            print(f"comanda necunoscuta: {step}")  # simbol invalid
            return False
        if step not in config['zones'][location]:
            print(f"nu exista cale din {location} folosind '{step}'")  # tranzitie inexistenta
            return False
        location = config['zones'][location][step]  # actualizeaza zona curenta
        print(f"te-ai deplasat in: {location}")

    # verifica daca zona finala este una de acceptare
    if location in config['accept']:
        print(f"\nmisiune indeplinita, ai ajuns in {location}")
        return True
    else:
        print(f"\nmisiune esuata, zona finala {location} nu este obiectiv")
        return False


# functie principala care porneste jocul
def start_game():
    print("simulator de misiune spatiala pornit")
    filepath = input("introdu numele fisierului de configurare: ").strip()

    try:
        config = parse_config(filepath)  # incearca sa incarce configuratia
    except Exception as e:
        print(f"eroare la citirea fisierului: {e}")  # afiseaza eroare daca fisierul nu e valid
        return

    # citeste de la utilizator secventa de comenzi
    command_sequence = input("introdu secventa de comenzi separate prin spatiu (secventa de a si b separate prin spatiu): ").strip()
    result = simulate_path(config, command_sequence)  # simuleaza executia

    # afiseaza rezultatul final
    print("\nrezultat final:", "succes" if result else "esec")


# executa jocul doar daca fisierul este rulat direct
if __name__ == "__main__":
    start_game()

# input-uri acceptate: a a, a b, a a a b a, a b a b
# input-uri respinse: b, a a c, a a b c
