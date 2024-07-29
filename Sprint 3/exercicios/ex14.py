def print_params(*naomeados, **nomeados):
    for arg in naomeados:
        print(arg)
    for arg in nomeados.values():
        print(arg)

print_params(1, 3, 4, 'hello', parametro_nomeado='alguma coisa', x=20)