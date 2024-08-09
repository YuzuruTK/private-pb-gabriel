def calc(calc: tuple):
    operation = calc[0]
    x, y = calc[1]

    match operation:
        case '+':
            return (x + y)
        case '-':
            return (x - y)
        case '*':
            return (x * y)
        case '/':
            return (x / y)
        case '%':
            return (x % y)
        case _:
            return 0
def calcular_valor_maximo(operadores,operandos) -> float:
    results = [*map(calc, zip(operadores, operandos))]

    return max(results)

operadores = ['+','-','*','/','+']
operandos  = [(3,6), (-7,4.9), (8,-8), (10,2), (8,4)]

print(calcular_valor_maximo(operadores, operandos))