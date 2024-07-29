class Passaro:
    def voar(self):
        print("Voando...")
        
    def emitir_som(self):
        pass

class Pato(Passaro):
    def emitir_som(self):
        print("Quack Quack")

class Pardal(Passaro):
    def emitir_som(self):
        print("Piu Piu")


pato = Pato()
pard = Pardal()

print("Pato")
pato.voar()
print("Pato emitindo som...")
pato.emitir_som()

print("Pardal")
pard.voar()
print("Pardal emitindo som...")
pard.emitir_som()