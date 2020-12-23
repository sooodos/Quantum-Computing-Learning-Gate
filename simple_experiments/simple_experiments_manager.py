import constants
from simple_experiments.hello_quantum_world import HelloWorld
from simple_experiments.interference import Interference
from simple_experiments.single_qubit_superposition import SingleQubitSuperposition
from simple_experiments.three_qubits_superposition import ThreeQubitSuperposition


class SimpleExperimentsManager:
    @classmethod
    def showcase(cls):
        print("Hi, these are the available experiments")

        for i in range(len(constants.experiments)):
            print(f"{i}. {constants.experiments[i]}")

        choice = input(f"Which experiment would you like to try from 0 to {len(constants.experiments)-1}? ")

        while choice not in constants.acceptable_experiment_inputs:
            choice = input(f"Which experiment would you like to try from 0 to {len(constants.experiments) - 1}? ")
        if choice == "0":
            HelloWorld.run()
        elif choice == "1":
            SingleQubitSuperposition.run()
        elif choice == "2":
            ThreeQubitSuperposition.run()
        elif choice == "3":
            Interference.run()

