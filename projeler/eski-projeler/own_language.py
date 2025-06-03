import operator

def run(program: list):
    comparison_operators = {"<": operator.lt, ">": operator.gt, "<=": operator.le, ">=": operator.ge, "==": operator.eq, "!=": operator.ne}
    result = []
    location_dictionary = {}
    instruction_id = 0
    instruction_list = []
    variables = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "U": 0, "V": 0, "W": 0, "X": 0, "Y": 0, "Z": 0}
    
    for line in program:
        instruction = line.split(" ")
        instruction_list.append(instruction)

    for i in range(len(instruction_list)):
        instruction = instruction_list[i]
        if instruction[0][-1] == ":":
            location = instruction[0][:-1]
            location_dictionary[location] = i + 1
            print("added location:",location,"with the id",i + 1)

    while instruction_id < len(program):
        instruction = instruction_list[instruction_id]

        match instruction[0]:
            case "PRINT":
                try:
                    result.append(variables[instruction[1]])
                except KeyError:
                    result.append(int(instruction[1]))
                instruction_id += 1
                print("print done")
            case "MOV":
                try:
                    variables[instruction[1]] = int(instruction[2])
                except ValueError:
                    variables[instruction[1]] = variables[instruction[2]]
                instruction_id += 1
                print("mov done")
            case "ADD":
                try:
                    variables[instruction[1]] += int(instruction[2])
                    instruction_id += 1
                    print("add1 done")
                except ValueError:
                    variables[instruction[1]] += variables[instruction[2]]
                    instruction_id += 1
                    print("add2 done")
            case "SUB":
                try:
                    variables[instruction[1]] -= int(instruction[2])
                    instruction_id += 1
                    print("sub1 done")
                except ValueError:
                    variables[instruction[1]] -= variables[instruction[2]]
                    instruction_id += 1
                    print("sub2 done")
            case "MUL":
                try:
                    variables[instruction[1]] *= int(instruction[2])
                    instruction_id += 1
                    print("mul1 done")
                except ValueError:
                    variables[instruction[1]] *= variables[instruction[2]]
                    instruction_id += 1
                    print("mul2 done")
            case "JUMP":
                instruction_id = location_dictionary[instruction[1]]
                print("jump done")
            case "IF":
                try:
                    first_value = int(instruction[1])
                except ValueError:
                    first_value = variables[instruction[1]]
                try:
                    second_value = int(instruction[3])
                except ValueError:
                    second_value = variables[instruction[3]]
                if comparison_operators[instruction[2]](first_value, second_value) == True:
                    instruction_id = location_dictionary[instruction[5]]
                    print("if1 done")
                else:
                    instruction_id += 1
                    print("if2 done")
            case "END":
                return result
            case _:
                print("initiated")
                instruction_id += 1

                
    return result

if __name__ == "__main__":
    pass