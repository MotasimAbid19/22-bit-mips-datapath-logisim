from os import read


def convertBinToHex(bin):
    hexval = hex(int(bin, 2))[2:]
    return hexval

def convertOpcode(op):
    opcodeDict = {
        "beq"  : "001",
        "nor"  : "000",
        "nop"  : "000",
        "addi" : "010",
        "lw"   : "011",
        "and"  : "000",
        "j"    : "110",
        "sub"  : "000",
        "sll"  : "000",
        "slt"  : "000",
        "sw"   : "100",
        "srl"  : "000",
        "bne"  : "101",
        "add"  : "000",
        "or"   : "000",
    }
    return opcodeDict[op]


def convertFunctionBits(funcBits):
    functionDict = {
        "nor": "0001",
        "nop": "0000",
        "and": "0010",
        "sub": "0011",
        "sll": "0100",
        "slt": "0101",
        "srl": "0110",
        "add": "0111",
        "or" : "1000",
    }
    return functionDict[funcBits]


def checkRegister(reg):
    registerNum = int(reg[1:])
    if registerNum > 22:
        print("Invalid register")
    return format(registerNum, "05b")


rtypeInstructions = [
    "nor",
    "nop",
    "and",
    "sub",
    "sll",
    "slt",
    "srl",
    "add",
    "or",
]

itypeInstructions = [
    "beq",
    "addi",
    "lw",
    "sw",
    "bne",
]

readf = open("inputs.txt", "r")
writef = open("outputs.raw", "w")
writef.write("v2.0 raw\n")

for line in readf:
    splitted = line.strip().split()
    
    if not splitted:  # Skip empty lines
        continue
    
    instruction = splitted[0]
    
    if instruction in rtypeInstructions:
        if len(splitted) != 4: 
            print(f"Invalid R-type instruction format: {line}")
            continue
        
        opcode = convertOpcode(instruction)
        funcBits = convertFunctionBits(instruction)
        rs = checkRegister(splitted[2])
        rt = checkRegister(splitted[3])
        rd = checkRegister(splitted[1])
        out = opcode + rs + rt + rd + funcBits
        print(out)
        writef.write(convertBinToHex(out) + "\n")

    elif instruction == "nop":
        out = "0000000000000000000000"  # All zeros for a 22-bit nop instruction
        print(out)
        writef.write(convertBinToHex(out) + "\n")

    elif instruction in itypeInstructions:
        if len(splitted) != 4:
            print(f"Invalid I-type instruction format: {line}")
            continue
        
        opcode = convertOpcode(instruction)
        rs = checkRegister(splitted[2])
        rd = checkRegister(splitted[1])
        im = format(int(splitted[3]), "09b")
        out = opcode + rs + rd + im
        print(out)
        writef.write(convertBinToHex(out) + "\n")

    elif instruction == "j":
        if len(splitted) != 2:  
            print(f"Invalid J-type instruction format: {line}")
            continue
        
        opcode = convertOpcode(instruction)
        target = format(int(splitted[1]), "019b")
        out = opcode + target
        print(out)
        writef.write(convertBinToHex(out) + "\n")

    else:
        print(f"Unknown instruction: {line}")