with open("Sprint 4/exercicios/number.txt", "r") as file:
    

    numbers = map(lambda x: int(x), file.readlines())
    numbers = sorted(numbers,reverse=True)

    even_numbers = list(filter(lambda value: value % 2 == 0, numbers))

    five_even_numbers = even_numbers[:5]

    summed_numbers = sum(five_even_numbers)

    print(five_even_numbers)
    print(summed_numbers)