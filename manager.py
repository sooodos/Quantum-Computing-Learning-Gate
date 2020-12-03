from qiskit import IBMQ

import constants
from tools import Tools


def print_answers(answer_of_simulation, answer_of_real, least_busy_backend, classical_answer, algorithm):
    print("****************** FINAL * RESULTS *******************")
    if answer_of_simulation is not None:
        Tools.print_simul(answer_of_simulation, algorithm)
        print("******************************************************")
    if answer_of_real is not None:
        Tools.print_real(answer_of_real, least_busy_backend, algorithm)
        print("******************************************************")
    if classical_answer is not None:
        Tools.print_classical_answer(classical_answer, algorithm)
        print("******************************************************")
    return


class Manager:
    if __name__ == '__main__':
        flag = "Y"
        while flag == "Y":
            answer_of_simulation = None
            answer_of_real = None
            least_busy_backend = None
            classical_answer = None

            algorithm = input(constants.input_message_1)
            while algorithm not in constants.acceptable_algorithm_inputs:
                algorithm = input(constants.input_message_1)

            execution = input(constants.input_message_2)
            while execution not in constants.acceptable_execution_inputs:
                execution = input(constants.input_message_2)

            if execution == "0":
                classical_answer = Tools.execute_classically(algorithm)
            elif execution == "1":
                answer_of_simulation = Tools.execute_in_simulator(algorithm)
            elif execution == "2":
                answer_of_real = Tools.execute_in_real_device(algorithm)
            elif execution == "3":
                combined = Tools.execute_both(algorithm)
            print_answers(answer_of_simulation, answer_of_real, least_busy_backend, classical_answer, algorithm)
            flag = input("Would you like to keep experimenting? (Y/N)")
        print()
        print("Your experimenting session is now concluded. \nThank you.")
