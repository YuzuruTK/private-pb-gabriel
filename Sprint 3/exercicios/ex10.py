lista = ['abc', 'abc', 'abc', '123', 'abc', '123', '123'] 

not_duplicated = set(lista).intersection(lista)

print(list(not_duplicated))