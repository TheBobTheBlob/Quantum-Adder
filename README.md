
# Quantum Adder

<p align="center">
  <img src=".github/shor.jpg" width="750" alt="Shor code circuit"/>
</p>

The final project for the Quantum Computing class (Physics 5001, Fall 2024) I took at Missouri S&T was to create a adder circuit and run it on a real quantum computing using IBM Quantum. As quantum computers have a lot of errors, Shor code error correction needed to be added to the adder circuit.

There are multiple jupyter notebooks that each have different circuits that were tested.

- `adder.ipynb`: The basic adder circuit, built using sum, carry, and inverse carry gates.
- `adder_corrected_end.ipynb`: The adder circuit where Shor error checking is only done once at the end of the whole circuit.
- `adder_corrected_all_gate.ipynb`: The adder circuit where the Shor error checking is done after every sum or carry operation.
- `adder_transversal.ipynb`: The adder circuit with transversal adder operations.

## Running the Notebooks

1. Install the required Python packages using a package manager. The list is available in `pyproject.toml`.
2. Create a `.env` file
3. Add the key `IBM` to the environment file. Set it equation to your API key from IBM Quanum
4. Run the notebook using jupyer.

```bash
jupyter notebook file.ipynb
```
