class Aviao:
    def __init__(self, modelo, velocidade_maxima, capacidade, cor):
        self.modelo = modelo
        self.velocidade_maxima = velocidade_maxima
        self.cor = cor
        self.capacidade = capacidade


avioes = []

avioes.append(Aviao("BOIENG456", 1500, 400, "Azul"))
avioes.append(Aviao("Embraer Praetor 600", 863, 14, "Azul"))
avioes.append(Aviao("Antonov An-2", 258, 12, "Azul"))

for aviao in avioes:
    print(f'O avião de modelo {aviao.modelo} possui uma velocidade máxima de {aviao.velocidade_maxima} km/h, capacidade para {aviao.capacidade} passageiros e é da cor {aviao.cor}.')
