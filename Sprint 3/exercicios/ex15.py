class Lampada:
    def __init__(self, ligada):
        self.ligada = ligada

    def liga(self):
        self.ligada = True

    def desliga(self):
        self.ligada = False
    
    def esta_ligada(self):
        return self.ligada
    

lamp = Lampada(False)

lamp.liga()
print(f"A lâmpada está ligada? {lamp.esta_ligada()}")
lamp.desliga()
print(f"A lâmpada ainda está ligada? {lamp.esta_ligada()}")