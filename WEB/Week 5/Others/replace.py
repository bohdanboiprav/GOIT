math_operators = {
    'A': '+',
    'B': '-',
    'C': '*',
    'D': '>',
    'E': '<',
    'F': '=',
    # Add more mappings as needed
}

a ="[8C2]IA101(EJ[16A4](A5](B3]"
b = '[16B7](B4][C6 (FIE1 1A41(C21'
c = '[9A21C2](B6](E][2C7](B7]'
d = '[4A4J|67](B4](F(4C6](A2)'
f = '(5C5JASJ(DJ[3C1 0](A81|B4]'

text = "A + B = C"

# Replace letters with operators
for letter, operator in math_operators.items():
    text = a.replace(letter, operator)
    print(text)
# Split the text into a list of strings