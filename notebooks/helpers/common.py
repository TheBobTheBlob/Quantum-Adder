import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit.visualization import plot_histogram
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import QuantumCircuit
import qiskit_aer
import qiskit
import qiskit_aer.primitives
from matplotlib.pyplot import Figure
from abc import ABC, abstractmethod

load_dotenv()


def max_count(counts: dict) -> str:
    """
    Given a dictionary of counts, return the key with the highest value
    """
    return max(counts, key=counts.get)


def simplify(state: str, mapping: list) -> str:
    """
    Given a state and a mapping, return the simplified state
    """
    simplified = ""
    for i in range(len(mapping)):
        if mapping[i]:
            simplified += state[i]

    return simplified


def logical_register(name: str) -> list:
    """
    Return a logical register made out of 9 physical qubits, with a name
    """
    return [qiskit.QuantumRegister(1, name), qiskit.QuantumRegister(8, f"{name}l")]



def plot_old_simulation(job: str, classical_name: str = "meas") -> Figure:
    service = QiskitRuntimeService(channel="ibm_quantum", instance="ibm-q/open/main", token=os.environ["IBM"])
    job = service.job("cx0dfvzpx23g008j891g")
    job_result = job.result()
    pub_result = job_result[0].data[classical_name].get_counts()

    return plot_histogram(pub_result)

class QuantumComputer(ABC):
    """
    Base class for quantum computers simulations
    """
    def __init__(self, circuit: QuantumCircuit, shots: int = 128):
        self.circuit = circuit
        self.shots = shots

        self.counts = None

    @abstractmethod
    def run(self) -> dict:
        pass

    def most_common(self) -> str:
        return max_count(self.counts)

    def simplified(self, mapping: list) -> str:
        return simplify(self.most_common(), mapping)

    def plot(self, filename: None | str = None) -> Figure:
        if self.counts is None:
            raise Exception("No counts to plot.")

        if filename:
            return plot_histogram(self.counts, filename=filename, figsize=(20, 10))
        else:
            return plot_histogram(self.counts)


class RealQuantumComputer(QuantumComputer):
    """
    Class to run a quantum circuit on a real quantum computer using IBM Quantum
    """
    def __init__(self, circuit: QuantumCircuit, shots: int = 128):
        super().__init__(circuit, shots)
        self.token = os.environ["IBM"]

        self.service = QiskitRuntimeService(channel="ibm_quantum", token=self.token)
        self.backend = self.service.least_busy(operational=True, simulator=False)

    def run(self, classical_name: str= "meas") -> dict:
        pm = generate_preset_pass_manager(backend=self.backend, optimization_level=1)
        isa_circuit = pm.run(self.circuit)

        sampler = SamplerV2(self.backend)
        job = sampler.run([isa_circuit], shots=self.shots)
        pub_result = job.result()[0]

        self.counts = pub_result.data[classical_name].get_counts()

        return self.counts

    def backend_name(self) -> str:
        return self.backend.name


class SimulatedQuantumComputer(QuantumComputer):
    """
    Class to run a quantum circuit on a simulator using Qiskit Aer
    """
    def __init__(self, circuit: QuantumCircuit, shots: int = 128):
        super().__init__(circuit, shots)

        self.backend = qiskit_aer.AerSimulator(method="statevector")
        self.sampler = qiskit_aer.primitives.SamplerV2()

    def run(self) -> dict:
        qc_transpiled = qiskit.transpile(self.circuit, self.backend)
        job = self.sampler.run([qc_transpiled], shots=self.shots)
        job_result = job.result()

        self.counts = list(job_result[0].data.values())[0].get_counts()

        return self.counts


class StopExecution(Exception):
    # Raise to avoid running on real quantum hardware accidentally
    def _render_traceback_(self):
        return []

