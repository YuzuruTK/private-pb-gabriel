def soma_tudo(lista_valores: str):
    lista_valores  = lista_valores.split(",")
    total = 0
    for number in lista_valores:
        total += int(number)
    return total

print(soma_tudo("1,3,4,6,10,76"))
