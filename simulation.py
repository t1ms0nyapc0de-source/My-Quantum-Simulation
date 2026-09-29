#import libraries
import qiskit
import numpy as np
import matplotlib.pylab as plt
import warnings
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import Statevector,SparsePauliOp
from qiskit.synthesis import (
    SuzukiTrotter,
    LieTrotter,
)
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
warnings.filterwarnings("ignore")

def get_hamiltonian(nqubits,J,h,alpha):

    ZZ_tuples = [("ZZ",[i, i+1],-J) for i in range(0,nqubits - 1)] 
    Z_tuples = [("Z",[i], -h*np.sin(alpha)) for i in range(0,nqubits)]
    X_tuples = [("X",[i], -h*np.cos(alpha)) for i in range(0,nqubits)]

    hamiltonian = SparsePauliOp.from_sparse_list(
         [*ZZ_tuples, *Z_tuples, *X_tuples], num_qubits=nqubits
    )
    return hamiltonian.simplify()

n_qubits = 6
hamiltonian = get_hamiltonian(nqubits=n_qubits, J=0.2, h=1.2, alpha=np.pi / 8.0)


num_timesteps=60
evolution_time = 30.0
dt =evolution_time / num_timesteps
product_formula_lt=LieTrotter()

initial_circuit =QuantumCircuit(n_qubits)
initial_circuit.prepare_state("001100")
#initial_circuit.decompose(reps=1).draw("mpl")

single_step_evolution_gates_lt =PauliEvolutionGate(
    hamiltonian, dt, synthesis=product_formula_lt
)
single_step_evolution_lt=QuantumCircuit(n_qubits)

single_step_evolution_lt.append(
    single_step_evolution_gates_lt, single_step_evolution_lt.qubits
)

magnetization = (
    SparsePauliOp.from_sparse_list(
        [("Z", [i], 1.0) for i in range(0, n_qubits)], num_qubits=n_qubits
    )
    / n_qubits
)
correlation = SparsePauliOp.from_sparse_list(
    [("ZZ", [i, i + 1], 1.0) for i in range(0, n_qubits - 1)], num_qubits=n_qubits
) / (n_qubits - 1)

evolved_state=QuantumCircuit(initial_circuit.num_qubits)
evolved_state.append(initial_circuit,evolved_state.qubits)
estimator=StatevectorEstimator()

shots = 10000
precision=np.sqrt(1/shots)
energy_list = []
mag_list = []
corr_list = []

job=estimator.run(
    [(evolved_state, [hamiltonian, magnetization, correlation])], precision=precision
)

evs =job.result()[0].data.evs

energy_list.append(evs[0])
mag_list.append(evs[1])
corr_list.append(evs[2])

for n in range(num_timesteps):
    evolved_state.append(single_step_evolution_gates_lt,evolved_state.qubits)

    job=estimator.run(
        [(evolved_state, [hamiltonian, magnetization, correlation])],
        precision=precision,
        )

    evs=job.result()[0].data.evs
    energy_list.append(evs[0])
    mag_list.append(evs[1])
    corr_list.append(evs[2])

energy_array = np.array(energy_list)
mag_array = np.array(mag_list)
corr_array = np.array(corr_list)





