from simple_experiments.hello_quantum_world import HelloWorld


class SimpleExperimentsManager:
    @classmethod
    def showcase(cls):
        print("Hi")
        HelloWorld.run_hello_world()
