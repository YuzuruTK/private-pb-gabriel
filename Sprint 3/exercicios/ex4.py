for test_number in range(1,100 + 1):
    divisions = 0 
    for div_number in range(1,test_number + 1):
        if test_number % div_number == 0:
            divisions += 1
    if divisions == 2:
        print(test_number)