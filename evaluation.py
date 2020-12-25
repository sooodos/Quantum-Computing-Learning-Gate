from classical.random_binary import RandomBinary
from tools import Tools
import constants
from qiskit.providers import JobStatus


class Evaluation:
    @classmethod
    def evaluate(cls, algorithm):

        if algorithm == "0":
            cls.evaluate_deutsch_josza()
        elif algorithm == "1":
            cls.evaluate_bernstein_vazirani()

    @classmethod
    def evaluate_deutsch_josza(cls):
        print(constants.input_message_3)
        test_range = int(input())
        while test_range > 14 or test_range < 1:
            test_range = int(input("Enter a number between 1 and 14."))

        circuits = []
        n_bits = []
        quantum_execution_times = []
        classical_execution_times = []

        print("Evaluating Deutsch - Josza... This might take a while...")

        for number_of_bits in range(1, test_range + 1):
            n_bits.append(number_of_bits)
            circuits.append(Tools.prepare_dj(number_of_bits))
            total_time = 0.0
            for i in range(1024):
                classical_result = Tools.deutsch_josza_classical(number_of_bits)
                total_time = total_time + classical_result[1]
            classical_execution_times.append(total_time)
            completion_percentage = int((number_of_bits / test_range) * 100)
            print(f"{completion_percentage}% of classical executions done.")

        print("Now looking for the least busy backend...")
        least_busy_backend = Tools.find_least_busy_backend_from_open(test_range)

        print("Now waiting for the Quantum Batch Job to finish...\n This will for sure take a while...")
        quantum_results = Tools.run_batch_job(circuits, least_busy_backend)
        flag = False
        while not flag:
            for status in quantum_results.statuses():
                flag = True
                if status != JobStatus.DONE:
                    flag = False

        print("Quantum experiments finished.")
        for job in quantum_results.managed_jobs():
            quantum_execution_times.append(job.result().time_taken)
            counts_dict = job.result().get_counts()
            print(type(counts_dict))
            # print(job.result().get_counts())

        import matplotlib.pyplot as plt
        plt.plot(n_bits, classical_execution_times, 'c')
        plt.plot(n_bits, quantum_execution_times, 'r')
        plt.ylabel('Time taken in seconds')
        plt.show()
        return

    @classmethod
    def evaluate_bernstein_vazirani(cls):
        print(constants.input_message_3)
        test_range = int(input())
        while test_range > 14 or test_range < 1:
            test_range = int(input("Enter a number between 1 and 14."))

        n_bits = []
        circuits = []
        quantum_execution_times = []
        classical_execution_times = []

        print("Evaluating Bernstein - Vazirani... This might take a while...")

        for number_of_bits in range(1, test_range + 1):
            n_bits.append(number_of_bits)
            classical_result = Tools.bernstein_vazirani_classical(number_of_bits)
            random_binary = RandomBinary.generate_random_binary_v2(number_of_bits)
            circuits.append(Tools.prepare_bv(random_binary))
            classical_execution_times.append(classical_result[1])
            completion_percentage = int((number_of_bits / test_range) * 100)
            print(f"{completion_percentage}% of preparation done.")

        print("Now looking for the least busy backend...")
        least_busy_backend = Tools.find_least_busy_backend_from_open(test_range)

        print("Now waiting for the Quantum Batch Job to finish...")
        quantum_results = Tools.run_batch_job(circuits, least_busy_backend).results()

        for number_of_bits in range(0, test_range):
            print(quantum_results.get_counts(number_of_bits))

        import matplotlib.pyplot as plt
        plt.plot(n_bits, classical_execution_times, 'c')
        plt.plot(n_bits, quantum_execution_times, 'r')
        plt.ylabel('Time taken in seconds')
        plt.show()
        return
