import qiskit

# Custom SUM gate
sum_qreg = qiskit.QuantumRegister(3, "q")
sum = qiskit.QuantumCircuit(sum_qreg, name="S")

sum.cx(sum_qreg[1], sum_qreg[2])
sum.cx(sum_qreg[0], sum_qreg[2])


# Custom CARRY gate
carry_qreg = qiskit.QuantumRegister(4, "q")
carry = qiskit.QuantumCircuit(carry_qreg, name="C")

carry.ccx(carry_qreg[1], carry_qreg[2], carry_qreg[3])
carry.cx(carry_qreg[1], carry_qreg[2])
carry.ccx(carry_qreg[0], carry_qreg[2], carry_qreg[3])


# Custom REVERSE CARRY gate
carry_dagger_qreg = qiskit.QuantumRegister(4, "q")
reverse_carry = qiskit.QuantumCircuit(carry_dagger_qreg, name="CD")

reverse_carry.ccx(carry_dagger_qreg[0], carry_dagger_qreg[2], carry_dagger_qreg[3])
reverse_carry.cx(carry_dagger_qreg[1], carry_dagger_qreg[2])
reverse_carry.ccx(carry_dagger_qreg[1], carry_dagger_qreg[2], carry_dagger_qreg[3])


# Custom SHOR SETUP gate
shor_setup_qreq = qiskit.QuantumRegister(9, "q")

shor_setup = qiskit.QuantumCircuit(shor_setup_qreq, name="SS")
shor_setup.cx(shor_setup_qreq[0], shor_setup_qreq[3])
shor_setup.cx(shor_setup_qreq[0], shor_setup_qreq[6])

shor_setup.h(shor_setup_qreq[0])
shor_setup.h(shor_setup_qreq[3])
shor_setup.h(shor_setup_qreq[6])

shor_setup.cx(shor_setup_qreq[0], shor_setup_qreq[1])
shor_setup.cx(shor_setup_qreq[0], shor_setup_qreq[1])
shor_setup.cx(shor_setup_qreq[3], shor_setup_qreq[4])
shor_setup.cx(shor_setup_qreq[3], shor_setup_qreq[5])
shor_setup.cx(shor_setup_qreq[6], shor_setup_qreq[7])
shor_setup.cx(shor_setup_qreq[6], shor_setup_qreq[8])


# Custom SHOR TEARDOWN gate
shor_teardown_qreg = qiskit.QuantumRegister(9, "q")
shor_teardown = qiskit.QuantumCircuit(shor_teardown_qreg, name="ST")

shor_teardown.cx(shor_teardown_qreg[0], shor_teardown_qreg[1])
shor_teardown.cx(shor_teardown_qreg[0], shor_teardown_qreg[2])
shor_teardown.ccx(shor_teardown_qreg[2], shor_teardown_qreg[1], shor_teardown_qreg[0])
shor_teardown.cx(shor_teardown_qreg[3], shor_teardown_qreg[4])
shor_teardown.cx(shor_teardown_qreg[3], shor_teardown_qreg[5])
shor_teardown.ccx(shor_teardown_qreg[5], shor_teardown_qreg[4], shor_teardown_qreg[3])
shor_teardown.cx(shor_teardown_qreg[6], shor_teardown_qreg[7])
shor_teardown.cx(shor_teardown_qreg[6], shor_teardown_qreg[8])
shor_teardown.ccx(shor_teardown_qreg[8], shor_teardown_qreg[7], shor_teardown_qreg[6])

shor_teardown.h(shor_teardown_qreg[0])
shor_teardown.h(shor_teardown_qreg[3])
shor_teardown.h(shor_teardown_qreg[6])

shor_teardown.cx(shor_teardown_qreg[0], shor_teardown_qreg[3])
shor_teardown.cx(shor_teardown_qreg[0], shor_teardown_qreg[6])
shor_teardown.ccx(shor_teardown_qreg[6], shor_teardown_qreg[3], shor_teardown_qreg[0])


def add_shor_setup(circuit, qubit: list):
    circuit.append(shor_setup, [qubit[0], *qubit[1]])
    return circuit


def add_shor_teardown(circuit, qubit: list):
    circuit.append(shor_teardown, [qubit[0], *qubit[1]])
    return circuit


def add_x(circuit, qubit: list):
    circuit.x(qubit[0])
    for qubit in qubit[1]:
        circuit.x(qubit)
    return circuit

def add_z(circuit, qubit: list):
    circuit.z(qubit[0])
    for qubit in qubit[1]:
        circuit.z(qubit)
    return circuit


def add_cx(circuit, qubit1: list, qubit2: list):
    circuit.cx(qubit1[0], qubit2[0])
    for i in range(8):
        circuit.cx(qubit1[1][i], qubit2[1][i])
    return circuit


def add_carry(circuit, qubit1: list, qubit2: list, qubit3: list, qubit4: list):
    circuit.append(carry, [qubit1[0], qubit2[0], qubit3[0], qubit4[0]])
    for i in range(8):
        circuit.append(carry, [qubit1[1][i], qubit2[1][i], qubit3[1][i], qubit4[1][i]])
    return circuit


def add_reverse_carry(circuit, qubit1: list, qubit2: list, qubit3: list, qubit4: list):
    circuit.append(reverse_carry, [qubit1[0], qubit2[0], qubit3[0], qubit4[0]])
    for i in range(8):
        circuit.append(reverse_carry, [qubit1[1][i], qubit2[1][i], qubit3[1][i], qubit4[1][i]])
    return circuit


def add_sum(circuit, qubit1: list, qubit2: list, qubit3: list):
    circuit.append(sum, [qubit1[0], qubit2[0], qubit3[0]])
    for i in range(8):
        circuit.append(sum, [qubit1[1][i], qubit2[1][i], qubit3[1][i]])
    return circuit