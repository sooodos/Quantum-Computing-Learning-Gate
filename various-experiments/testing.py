from classical.random_binary import RandomBinary


class Testing:
    decimals = int(input("Give the upper limit of the random number: "))
    random_decimal = RandomBinary.generate_random_binary(decimals)
    print(random_decimal)
