# Chord DHT implementation and analysis

An in-memory Python implementation of the Chord distributed hash table algorithm. It models a ring of nodes and supports joining, leaving, key insertion, and lookup. The notebooks and report analyze these operations using a computer-scientist dataset collected from Wikipedia.

This is an algorithm simulation: nodes are Python objects in one process, not networked peers.

## Run the tests

Use Python 3.11 or newer from the repository root:

```bash
python -m unittest discover -s tests -p 'test_chord_*.py'
```

## Explore the analysis

Create a virtual environment and install the notebook dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
jupyter notebook notebooks/chord_dht_analysis.ipynb
```

The range-query notebook is at `notebooks/chord_dft_range_queries.ipynb`. Generated analysis files are in `report/`.

## Repository layout

- `src/chord_dht/`: Chord ring, node, and lookup logic
- `src/crawler/`: Wikipedia data collection utilities
- `tests/`: joining, leaving, insertion, lookup, and node tests
- `data/`: raw and processed computer-scientist data used by the notebooks
- `report/`: analysis output and LaTeX report

## License

[MIT](LICENCE).
