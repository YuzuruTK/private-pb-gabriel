words = ['maça', 'arara', 'audio', 'radio', 'radar', 'moto']

for word in words:
    reverse_word = list(word)
    reverse_word.reverse()
    reverse_word = ''.join(reverse_word)

    if word == reverse_word:
        print(f"A palavra: {word} é um palíndromo")
    else:
        print(f"A palavra: {word} não é um palíndromo")