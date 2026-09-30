#import libraries
import qiskit
import numpy as np
import matplotlib.pylab as plt
import warnings
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import (
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

#initialization
n_qubit_2=2
dt_2=1.6
product_formula=LieTrotter(reps=1)

initial_circuit_2=QuantumCircuit(n_qubit_2)
initial_circuit_2.prepare_state("10")

bar_width=0.1
final_time=1.6
eps = 1e-5
alphas = np.linspace(-np.pi / 2 + eps, np.pi / 2 - eps, 5)

#circuit
circuit_list=[]
for i,alpha in enumerate(alphas):
    evolved_state_2 =QuantumCircuit(initial_circuit_2.num_qubits)
    evolved_state_2.append(initial_circuit_2,evolved_state_2.qubits)
    hamiltonian_2 =get_hamiltonian(nqubits=2,J=0.2,h=1.0,alpha=alpha)
    single_step_evolution_gates_2=PauliEvolutionGate(hamiltonian_2,dt_2,synthesis=product_formula)
    evolved_state_2.append(single_step_evolution_gates_2,evolved_state_2.qubits)
    evolved_state_2.measure_all()
    circuit_list.append(evolved_state_2)
    
#Qiskit runtime config
QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="Your API ",
    instance="Your instance here",
    overwrite=True,
    set_as_default=True,
)


#connect to ibm hardware
service=QiskitRuntimeService()
backend = service.least_busy(operational=True,simulator=False)
pm = generate_preset_pass_manager(backend=backend, optimization_level=3)

circuit_isa=pm.run(circuit_list)
sampler = SamplerV2(mode=backend)
job = sampler.run(circuit_isa)


job_id = job.job_id()
results=job.result()
print("job id:", job_id)

#post-process result
list_temp = ["00", "01", "10", "11"]

for i, alpha in enumerate(alphas):
    # Dictionary of probabilities
    amplitudes_dict = results[i].data.meas.get_counts()
    values = []
    for str_temp in list_temp:
        values.append(
            amplitudes_dict.get(str_temp,0) / 4096.0
        )  # divided by default number of shots
    # Convert angle to degrees
    alpha_str = f"$\\alpha={int(np.round(alpha * 180 / np.pi))}^\\circ$"
    plt.bar(np.arange(4) + i * bar_width, values, bar_width, label=alpha_str, alpha=0.7)

plt.xticks(np.arange(4) + 2 * bar_width, list_temp)
plt.xlabel("Measurement")
plt.ylabel("Probabilities")
plt.suptitle(
    f"Measurement probabilities at $t={final_time}$, for various field angles $\\alpha$\n"
    f"Initial state: 10, Linear lattice of size $L=2$"
)
plt.legend()
plt.show()