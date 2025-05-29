def read_tape(file_path):
    with open(file_path, "r") as file:
        return list(file.read().strip())

def write_tape(file_path, tape):
    with open(file_path, "w") as file:
        file.write("".join(tape))

def turing_machine(tape):
    index = 0
    while tape[index] != "$":
        index += 1  # Găsim simbolul '$'
    
    index += 1  # Mergem la următorul spațiu liber '_'
    
    while tape[index] == "_":
        index += 1  # Găsim primul '#'
    
    index += 1  # Mergem după primul '#'
    
    copy_index = 0
    while tape[copy_index] != "$":
        tape[index] = tape[copy_index]
        copy_index += 1
        index += 1
    
    write_tape("tape.txt", tape)

# Citim și procesăm banda
tape = read_tape("tape.txt")
turing_machine(tape)

print("Procesare finalizată! Verifică 'tape.txt'.")
