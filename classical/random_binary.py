import random


class RandomBinary:

    @classmethod
    def generate_random_binary(cls, limit: int) -> str:
        rand = int(random.uniform(0, limit))
        print(f"random binary in decimal:{rand}")
        random_bin = bin(rand)[2:]
        print(random_bin)
        return random_bin
