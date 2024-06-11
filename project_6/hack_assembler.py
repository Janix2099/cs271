# Joey Taylor
# 6/10/2024
# Project 6
# File: hack_assembler.py
# Purpose: Build a hack assembler in Python using the base given by Joseph Jess in Session 12

import sys

def generate_machine_code(line: str, comp_lookup: dict, dest_lookup: dict, jump_lookup: dict, symbol_table: dict, ram_address: list) -> str:
    # Check if it's an A-instruction (starts with '@')
    if line.startswith('@'):
        value = line[1:]  # Get the value after '@'
        if value.isdigit():
            address = int(value)  # Direct address if it's a number
        else:
            if value not in symbol_table:
                # Assign a new RAM address if the symbol is not in the table
                symbol_table[value] = ram_address[0]
                ram_address[0] += 1
            address = symbol_table[value]
        return '0' + f'{address:015b}'  # Convert to binary and pad to 15 bits
    else:
        # It's a C-instruction
        dest, comp, jump = "null", line, "null"
        
        if '=' in line:
            dest, comp = line.split('=')  # Split dest and comp
        if ';' in comp:
            comp, jump = comp.split(';')  # Split comp and jump

        comp_bits = comp_lookup[comp]
        dest_bits = dest_lookup[dest]
        jump_bits = jump_lookup[jump]

        return '111' + comp_bits + dest_bits + jump_bits  # Combine for final instruction

def init_jump_lookup_dict() -> dict:
      # build jump lookup dictionary as a jump type (as a string) as the key and its dest bits (as a string) as value
    return {
        "null": "000",
        "JGT":  "001",
        "JEQ":  "010",
        "JGE":  "011",
        "JLT":  "100",
        "JNE":  "101",
        "JLE":  "110",
        "JMP":  "111",
    }

def init_dest_lookup_dict() -> dict:
    # build dest lookup dictionary as a dest register (as a string) as the key and its dest bits (as a string) as value
    return {
        "null": "000",
        "M":    "001",
        "D":    "010",
        "MD":   "011",
        "A":    "100",
        "AM":   "101",
        "AD":   "110",
        "AMD":  "111",
    }

def init_comp_lookup_dict() -> dict:
    # build comp lookup dictionary as a comp instruction (as a string) as the key and its control bits (as a string) as value
    return {
        "0":   "0101010",
        "1":   "0111111",
        "-1":  "0111010",
        "D":   "0001100",
        "A":   "0110000",
        "!D":  "0001101",
        "!A":  "0110001",
        "-D":  "0001111",
        "-A":  "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M":   "1110000",
        "!M":  "1110001",
        "-M":  "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }

def parse(input_line: str) -> str:
    # Remove comments / whitespace
    return input_line.split("//")[0].strip()

def build_symbol_table(lines: list) -> dict:
    # Initialize symbol table with predefined symbols
    symbol_table = {
        'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
        'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
        'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
        'SCREEN': 16384, 'KBD': 24576
    }
    line_number = 0
    for line in lines:
        if line.startswith('(') and line.endswith(')'):
            # Label declaration (e.g., (LOOP))
            label = line[1:-1]
            symbol_table[label] = line_number
        else:
            line_number += 1
    return symbol_table

def main():
    input_filename = sys.argv[1]  # Get input file name from command line
    output_filename = input_filename.replace('.asm', '.hack')  # Output file name
    
    # Read the input file
    with open(input_filename, "r") as input_file:
        input_file_contents = input_file.readlines()

    # Parse lines and remove empty lines/comments
    parsed_lines = [parse(line) for line in input_file_contents if parse(line)]
    
    # Build the symbol table with label definitions
    symbol_table = build_symbol_table(parsed_lines)

    # Initialize lookup dictionaries for comp, dest, and jump instructions
    comp_lookup = init_comp_lookup_dict()
    dest_lookup = init_dest_lookup_dict()
    jump_lookup = init_jump_lookup_dict()
    ram_address = [16]  # Starting address for variables in RAM

    # Remove label declarations from parsed lines
    parsed_lines = [line for line in parsed_lines if not (line.startswith('(') and line.endswith(')'))]

    # Generate machine code for each line
    machine_code_lines = [generate_machine_code(line, comp_lookup, dest_lookup, jump_lookup, symbol_table, ram_address) for line in parsed_lines]

    # Write the machine code to the output file
    with open(output_filename, "w") as output_file:
        for line in machine_code_lines:
            output_file.write(line + "\n")

if __name__ == "__main__":
    main()
