import functools

lancamentos = [
        (200,'D'),
        (300,'C'),
        (100,'C')
    ]

def calcula_saldo(lancamentos) -> float:
    valores = [*map(lambda x: -x[0] if x[1] == 'D' else x[0], lancamentos)]

    saldo = functools.reduce(lambda x, y: x + y, valores)
    
    return saldo

print(calcula_saldo(lancamentos=lancamentos))
    