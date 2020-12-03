from classical.random_binary import RandomBinary


class GuessBinary:

    @classmethod
    def guess_number(cls, random_binary):

        mask = 1
        guess = ""
        attempts = 0
        for bit in random_binary:
            hit = int(bit) & mask
            guess += str(hit)
            attempts += 1
        return f"My guess After {attempts} attempts is:\n{guess}."
