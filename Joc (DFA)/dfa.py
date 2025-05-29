def parse_config(path):
    # incarca configuratia unui dfa dintr-un fisier text
    with open(path, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith('#')]

    config = {
        'zones': {},
        'alphabet': [],
        'start': '',
        'accept': set(),
        'links': []
    }

    current_section = None

    for line in lines:
        if line.startswith("states:"):
            current_section = 'states'
            zone_names = line.split(":")[1].split()
            for name in zone_names:
                config['zones'][name] = {}
        elif line.startswith("alphabet:"):
            config['alphabet'] = line.split(":")[1].split()
        elif line.startswith("start:"):
            config['start'] = line.split(":")[1].strip()
        elif line.startswith("accept:"):
            config['accept'] = set(line.split(":")[1].split())
        elif line.startswith("transitions:"):
            current_section = 'transitions'
        elif current_section == 'transitions':
            src, symbol, dst = line.split()
            config['zones'][src][symbol] = dst

    return config


def simulate_path(config, path):
    # executa o secventa de actiuni si verifica daca misiunea a fost finalizata cu succes
    location = config['start']
    actions = path.strip().split()

    print(f"\nincepi misiunea din zona: {location}")

    for step in actions:
        if step not in config['alphabet']:
            print(f"comanda necunoscuta: {step}")
            return False
        if step not in config['zones'][location]:
            print(f"nu exista cale din {location} folosind '{step}'")
            return False
        location = config['zones'][location][step]
        print(f"te-ai deplasat in: {location}")

    if location in config['accept']:
        print(f"\nmisiune indeplinita, ai ajuns in {location}")
        return True
    else:
        print(f"\nmisiune esuata, zona finala {location} nu este obiectiv")
        return False


def start_game():
    print("simulator de misiune spatiala pornit")
    filepath = input("introdu numele fisierului de configurare: ").strip()

    try:
        config = parse_config(filepath)
    except Exception as e:
        print(f"eroare la citirea fisierului: {e}")
        return

    command_sequence = input("introdu secventa de comenzi separate prin spatiu (secventa de a si b separate prin spatiu): ").strip()
    result = simulate_path(config, command_sequence)

    print("\nrezultat final:", "succes" if result else "esec")


if __name__ == "__main__":
    start_game()
# input-uri acceptate: a a, a b, a a a b a, a b a b
# input-uri respinse: b, a a c, a a b c