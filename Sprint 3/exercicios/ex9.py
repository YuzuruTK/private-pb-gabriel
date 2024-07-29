primeirosNomes = ['Joao', 'Douglas', 'Lucas', 'José']
sobreNomes = ['Soares', 'Souza', 'Silveira', 'Pedreira']
idades = [19, 28, 25, 31]

persons = zip(primeirosNomes,sobreNomes,idades)

for index, person in enumerate(persons):
    print(f"{index} - {person[0]} {person[1]} está com {person[2]} anos")