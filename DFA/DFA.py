def citeste_dfa(drum_fisier):
    with open(drum_fisier, 'r') as fisier:
        linii = [linie.strip() for linie in fisier if linie.strip() and not linie.startswith('#')]

    configuratie = {
        'stari': set(),
        'alfabet': set(),
        'start': None,
        'finale': set(),
        'tranzitii': {}
    }

    sectiune_curenta = None

    for linie in linii:
        if linie.startswith('[') and linie.endswith(']'):
            sectiune_curenta = linie[1:-1]
            continue

        if sectiune_curenta == 'States':
            bucati = linie.split(',')
            stare = bucati[0]
            configuratie['stari'].add(stare)
            if len(bucati) > 1:
                marcaje = bucati[1:]
                if 'S' in marcaje:
                    configuratie['start'] = stare
                if 'A' in marcaje:
                    configuratie['finale'].add(stare)

        elif sectiune_curenta == 'Alphabet':
            configuratie['alfabet'].update(linie.strip())

        elif sectiune_curenta == 'Transitions':
            sursa, simbol, destinatie = map(str.strip, linie.split(','))
            if sursa not in configuratie['tranzitii']:
                configuratie['tranzitii'][sursa] = {}
            configuratie['tranzitii'][sursa][simbol] = destinatie

    return configuratie


def simuleaza_dfa(text, dfa):
    stare = dfa['start']
    for caracter in text:
        if caracter not in dfa['tranzitii'].get(stare, {}):
            return False
        stare = dfa['tranzitii'][stare][caracter]
    return stare in dfa['finale']


# Exemplu de rulare
dfa = citeste_dfa('DFA.txt')
cuvinte_test = ['1001', '1100', '101', '11111', '00', '0001011']

for cuvant in cuvinte_test:
    rezultat = simuleaza_dfa(cuvant, dfa)
    mesaj = "acceptat" if rezultat else "respins"
    print(f"{cuvant} este {mesaj} de automat.")
