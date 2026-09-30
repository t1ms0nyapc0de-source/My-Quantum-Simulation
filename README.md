# My-Quantum-Simulation
Simulation of trotterization for the transverse field Ising Hamiltonian

QNA:
1)What is trotterization?
Ans:Trotterization is a method used in quantum computing to approximate the time evolution of a quantum system by breaking down a complex, multi-part Hamiltonian into a sequence of simpler, manageable quantum gates

2)What is transverse field Ising Hamiltonian for?
Ans:The transverse-field Ising model is a simple spin model used mainly to study how quantum fluctuations compete with spin-spin interactions: the coupling J pushes spins to align, while the transverse field h scrambles them, producing a zero-temperature quantum phase transition at J ≈ h. It also serves as the standard baseline for studying quantum magnetism and entanglement, and it's a popular benchmark for simulating quantum dynamics and testing quantum annealers such as D-Wave's.

3)What is "Hamiltonian"?
Ans:The Hamiltonian of a system is an operator corresponding to the total energy of that system, including both kinetic energy and potential energy.

4)What is the model behind of Transverse Field Ising Hamiltonian?
Ans:Ising model. The Ising model is a simple model of many tiny magnets, called spins, arranged on a line or grid. Each spin can point only up or down (+1 or -1) and mostly cares about its neighbors. The energy is H = -J Σ sᵢsⱼ - h Σ sᵢ
where the first sum runs over neighboring pairs. If J is positive, neighbors prefer to point the same way, and h is an external field that nudges all spins in one direction. At low temperature the spins line up and form a magnet, while at high temperature thermal jiggling scrambles them. Between the two there is a sharp transition at a critical temperature, which is the model's most important feature. It is also one of the few interacting systems that can be solved exactly, in one dimension and in two (Onsager's solution).Because it's so simple, it shows up well beyond magnets. In physics and materials science it explains how a magnet loses its magnetization when heated, and it describes binary alloys (two kinds of atoms ordering on a lattice) and the "lattice gas" picture of a liquid boiling, where up and down stand for occupied and empty sites. In computing, neural networks such as Hopfield networks and Boltzmann machines are built on the same energy idea, and many hard optimization problems (scheduling, routing, graph partitioning) can be rewritten as finding the lowest-energy Ising configuration, which is what quantum annealers like D-Wave's try to do. Outside physics, it has been used as a toy model for how opinions spread in a population, for neurons firing or staying silent, and for sudden tipping points in ecosystems or climate, though those are analogies, not exact descriptions.

5)Why using Quantum Computer for the simulation?
Ans:It is for learning purposes, it is easy to simulate on quantum computer but it ran faster on Classical computer.I learnt about the workflow of Quantum Computer simulation, libraries, environment setup and configuration, and several quantum mechanism from this project. In shorts,it is just for fun.....

Reference Link=https://quantum.cloud.ibm.com/learning/en/courses/utility-scale-quantum-computing/quantum-simulation#4-executing-on-the-quantum-hardware
