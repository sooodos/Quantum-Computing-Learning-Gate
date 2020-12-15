import constants
from simple_experiments.simple_experiments_manager import SimpleExperimentsManager
from Algorithms.algorithms_manager import AlgorithmsManager


class Manager:
    if __name__ == '__main__':
        flag = "Y"
        while flag == "Y":

            choice = input("Press E for some simpler Experiments\nor press A for Algorithm Experimentation: ")
            while choice not in constants.acceptable_choice_inputs:
                choice = input("Press E for some simpler Experiments\nor press A for Algorithm Experimentation: ")

            if choice == "E":
                SimpleExperimentsManager.showcase()
            else:
                AlgorithmsManager.showcase()

            flag = input("Would you like to keep experimenting? (Y/N)")
            while flag is not "Y" or flag is not "N":
                flag = input("Would you like to keep experimenting? Please give a valid response. (Y/N)")
        print("\nYour experimenting session is now concluded. \nThank you.")
