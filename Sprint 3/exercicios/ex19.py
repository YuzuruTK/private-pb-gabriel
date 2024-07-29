import random

def calcular_media(lista):
    return sum(lista)/len(lista)

def calcular_mediana(lista):
    lista.sort()
    
    meio = (len(lista) -1) // 2

    if len(lista) % 2 == 0:
        mediana = (lista[meio] + lista[meio + 1]) / 2
    else:
        mediana = lista[meio]

    return mediana

def calcular_valor_maximo(lista):
    lista.sort()

    return max(lista)

def calcular_valor_minimo(lista):
    lista.sort()
    
    return min(lista)


random_list = random.sample(range(500), 50)

mediana = calcular_mediana(random_list)
media = calcular_media(random_list)
valor_minimo = calcular_valor_minimo(random_list)
valor_maximo = calcular_valor_maximo(random_list)

print(f"Media: {media}, Mediana: {mediana}, Mínimo: {valor_minimo}, Máximo: {valor_maximo}")