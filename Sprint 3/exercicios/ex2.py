numeros = []

for i in range(3):
    numeros.append(i)
    if i % 2 == 0:
        print(f"Par: {i}")
    else: 
        print(f"Ímpar: {i}")