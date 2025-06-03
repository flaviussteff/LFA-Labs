# functie care citeste configuratia unui dfa dintr-un fisier
def citeste_dfa(drum_fisier):
    # deschide fisierul si citeste liniile, ignorand comentariile si liniile goale
    with open(drum_fisier, 'r') as fisier:
        linii = [linie.strip() for linie in fisier if linie.strip() and not linie.startswith('#')]

    # initializeaza structura dfa-ului
    configuratie = {
        'stari': set(),          # multimea starilor
        'alfabet': set(),        # alfabetul de intrare
        'start': None,           # starea initiala
        'finale': set(),         # multimea starilor finale
        'tranzitii': {}          # dictionar de tranzitii
    }

    sectiune_curenta = None  # retine ce sectiune se parcurge (States, Alphabet, Transitions)

    # parcurge fiecare linie din fisier
    for linie in linii:
        # detecteaza inceputul unei noi sectiuni
        if linie.startswith('[') and linie.endswith(']'):
            sectiune_curenta = linie[1:-1]
            continue

        # proceseaza starile
        if sectiune_curenta == 'States':
            bucati = linie.split(',')        # imparte linia in stare si marcaje
            stare = bucati[0]                # prima bucata e numele starii
            configuratie['stari'].add(stare) # adauga starea la multimea de stari
            if len(bucati) > 1:
                marcaje = bucati[1:]         # restul sunt marcaje (S sau A)
                if 'S' in marcaje:
                    configuratie['start'] = stare    # seteaza starea initiala
                if 'A' in marcaje:
                    configuratie['finale'].add(stare) # adauga la starile de acceptare

        # proceseaza alfabetul
        elif sectiune_curenta == 'Alphabet':
            configuratie['alfabet'].update(linie.strip())  # adauga fiecare caracter din linie la alfabet

        # proceseaza tranzitiile
        elif sectiune_curenta == 'Transitions':
            sursa, simbol, destinatie = map(str.strip, linie.split(','))  # extrage sursa, simbol si destinatie
            if sursa not in configuratie['tranzitii']:
                configuratie['tranzitii'][sursa] = {}  # initializeaza dictionarul pentru sursa
            configuratie['tranzitii'][sursa][simbol] = destinatie  # seteaza tranzitia pentru simbol

    return configuratie  # returneaza configuratia completa a dfa-ului


# functie care simuleaza rularea unui dfa pe un sir dat
def simuleaza_dfa(text, dfa):
    stare = dfa['start']  # porneste din starea initiala
    for caracter in text:
        # verifica daca exista o tranzitie pentru simbolul curent din starea curenta
        if caracter not in dfa['tranzitii'].get(stare, {}):
            return False  # daca nu exista tranzitie, sirul e respins
        stare = dfa['tranzitii'][stare][caracter]  # actualizeaza starea curenta
    return stare in dfa['finale']  # verifica daca s-a ajuns intr-o stare finala


# exemplu de rulare
dfa = citeste_dfa('DFA.txt')  # citeste configuratia dfa-ului din fisier

# lista de cuvinte de test
cuvinte_test = ['1001', '1100', '101', '11111', '00', '0001011']

# simuleaza dfa pe fiecare cuvant si afiseaza rezultatul
for cuvant in cuvinte_test:
    rezultat = simuleaza_dfa(cuvant, dfa)  # verifica daca cuvantul este acceptat
    mesaj = "acceptat" if rezultat else "respins"  # decide mesajul in functie de rezultat
    print(f"{cuvant} este {mesaj} de automat.")  # afiseaza rezultatul
