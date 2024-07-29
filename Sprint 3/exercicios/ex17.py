def split_lista(lista: list):
    tam = len(lista)
    corte = int(tam/3)

    listao = []
    for _i in range(3):
        part = []
        for _one in range(corte):
            part.append(lista.pop(0))
        listao.append(part)
    stringao = ""
    for i in listao:
        stringao += f"{i} " 
    return stringao.rstrip(" ")

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 

listao = split_lista(lista)


print(listao)