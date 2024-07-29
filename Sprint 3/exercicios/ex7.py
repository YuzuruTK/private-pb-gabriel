a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
odd_numbers = []

for i in a:
    if i % 2 != 0:
        odd_numbers.append(i)
print(odd_numbers)