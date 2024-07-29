def my_map(list, f):
    return f(list)

def function(list):
    returned_list = []
    for i in list:
        returned_list.append(i ** 2) 
    return returned_list

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(my_map(lista, function))