from datetime import datetime

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, BasicAer, execute, IBMQ
from qiskit.providers import BaseJob
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram

import constants
from Algorithms.bernstein_vazirani import BernsteinVazirani
from Algorithms.deutsch_josza import DeutschJosza

from classical.classical_xor import ClassicalXor
from classical.guess_binary import GuessBinary
from classical.random_binary import RandomBinary


class Tools:
    @classmethod
    def calculate_elapsed_time(cls, first_step: datetime, last_step: datetime):
        difference = last_step - first_step
        return difference.total_seconds()

    @classmethod
    def run_on_simulator(cls, circuit: QuantumCircuit):
        # use local simulator
        backend = BasicAer.get_backend('qasm_simulator')
        shots = 1024
        results = execute(circuit, backend=backend, shots=shots).result()
        answer = results.get_counts()
        max_value = 0
        max_key = ""
        for key, value in answer.items():
            if value > max_value:
                max_value = value
                max_key = key
        return max_key[::-1]

    @classmethod
    def run_on_real_device(cls, circuit: QuantumCircuit, least_busy_backend):

        from qiskit.tools.monitor import job_monitor
        shots = 1
        job = execute(circuit, backend=least_busy_backend, shots=shots, optimization_level=3)
        job_monitor(job, interval=2)
        return job

    @classmethod
    def find_least_busy_backend_from_open(cls, n):
        IBMQ.load_account()
        provider = IBMQ.get_provider(hub='ibm-q')
        return least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= n and
                                                              not x.configuration().simulator and x.status().operational == True))

    @classmethod
    def find_least_busy_backend_from_research(cls, n):
        provider = IBMQ.get_provider(hub='ibm-q-research', group='Demetris-Zeinali', project='main')
        return least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= n and
                                                              not x.configuration().simulator and x.status().operational == True))

    @classmethod
    def print_simul(cls, answer_of_simul, algorithm: str):
        print(constants.algorithms[int(algorithm)])
        print("\nMeasurements: ", answer_of_simul)
        return

    @classmethod
    def print_real(cls, job: BaseJob, least_busy_backend, algorithm: str):
        results = job.result()
        answer = results.get_counts()
        print("\nTotal count for 00 and 11 are:", answer)
        elapsed = results.time_taken
        print(f"The time it took for the experiment to complete after validation was {elapsed} seconds")
        plot_histogram(data=answer, title=f"{constants.algorithms[int(algorithm)]} on {least_busy_backend}")
        plt.show()
        return

    @classmethod
    def execute_classically(cls, algorithm):
        if algorithm == "0":
            return cls.execute_deutsch_josza_classically()
        elif algorithm == "1":
            return cls.execute_bernstein_vazirani_classically()

    @classmethod
    def execute_in_simulator(cls, algorithm):
        dj_circuit = None
        if algorithm == "0":
            bits = str(input("Enter a bit sequence for the quantum circuit:"))
            dj_circuit = DeutschJosza.deutsch_josza(bits)
        elif algorithm == "1":
            decimals = int(input("Give the upper limit of the random number: "))
            random_binary = RandomBinary.generate_random_binary(decimals)
            dj_circuit = BernsteinVazirani.bernstein_vazirani(random_binary)
        return cls.run_on_simulator(dj_circuit)

    @classmethod
    def execute_in_real_device(cls, algorithm):

        if algorithm == "0":
            answer = cls.execute_dj_in_real_device()
            return answer
        elif algorithm == "1":
            decimals = int(input("Give the upper limit of the random number: "))
            random_binary = RandomBinary.generate_random_binary(decimals)
            answer = cls.execute_bv_in_real_device(random_binary)
            return answer

    @classmethod
    def execute_dj_in_real_device(cls):
        bits = str(input("Enter a bit sequence for the quantum circuit:"))
        least_busy_backend = Tools.choose_from_provider(len(bits) + 1)
        dj_circuit = DeutschJosza.deutsch_josza(bits)
        answer_of_real = Tools.run_on_real_device(dj_circuit, least_busy_backend)
        print(f"least busy is {least_busy_backend}")
        return answer_of_real

    @classmethod
    def execute_bv_in_real_device(cls, random_binary: str):
        dj_circuit = BernsteinVazirani.bernstein_vazirani(random_binary)
        least_busy_backend = Tools.choose_from_provider(dj_circuit.qubits)
        answer_of_real = Tools.run_on_real_device(dj_circuit, least_busy_backend)
        print(f"least busy is {least_busy_backend}")
        return answer_of_real

    @classmethod
    def choose_from_provider(cls, size: int):
        least_busy_backend = None
        research = input("Do you want to run this experiment on the research backends? (Y/N)")
        while research != "Y" and research != "N":
            research = input("Do you want to run this experiment on the research backends? (Y/N)")
        if research == "N":
            least_busy_backend = Tools.find_least_busy_backend_from_open(size)
        elif research == "Y":
            least_busy_backend = Tools.find_least_busy_backend_from_research(size)
        return least_busy_backend

    @classmethod
    def execute_deutsch_josza_classically(cls):
        number_of_bits = int(input("Enter number of bits for a the classical solution:"))
        return ClassicalXor.execute_classical_xor(bits=number_of_bits)

    @classmethod
    def execute_bernstein_vazirani_classically(cls):
        decimals = int(input("Give the upper limit of the random number: "))
        random_binary = RandomBinary.generate_random_binary(decimals)
        return GuessBinary.guess_number(random_binary)

    @classmethod
    def print_classical_answer(cls, classical_answer, algorithm):
        print(f"Results of classical implementation for the {constants.algorithms[int(algorithm)]} Algorithm:")
        print(classical_answer)

    @classmethod
    def execute_both(cls, algorithm):
        answer = []
        if algorithm == "0":
            classical = cls.execute_deutsch_josza_classically()
            real = cls.execute_dj_in_real_device()
            answer.append(classical)
            answer.append(real)
        elif algorithm == " 1":
            classical = cls.execute_bernstein_vazirani_classically()
            real = cls.execute_bv_in_real_device(classical)
            answer.append(classical)
            answer.append(real)
        return answer
