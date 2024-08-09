vogals = ['a','e','i','o','u']

def conta_vogais(texto:str)-> int:
    
    letters = list(texto)

    filtration = filter(lambda x: x.lower() in vogals, letters)

    vogals_on_word = list(filtration)

    return len(vogals_on_word)

print(conta_vogais("Ola mundo, este e um importante teste"))