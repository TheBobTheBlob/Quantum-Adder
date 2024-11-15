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
    Given a dictionary of counts, return the key with the highest value.
    """
    return max(counts, key=counts.get)


def simplify(state: str, mapping: list) -> str:
    """
    Given a state and a mapping, return the simplified state.
    """
    simplified = ""
    for i in range(len(mapping)):
        if mapping[i]:
            simplified += state[i]

    return simplified


class QuantumComputer(ABC):
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

    def plot(self) -> Figure:
        if self.counts is None:
            raise Exception("No counts to plot.")

        return plot_histogram(self.counts)


class RealQuantumComputer(QuantumComputer):
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

