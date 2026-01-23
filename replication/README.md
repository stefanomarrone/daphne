# Replication Package

This directory provides a minimal and self-contained replication package
to reproduce an example run of the data acquisition pipeline implemented
in the DAPHNE module.

The goal of this package is to demonstrate how the proposed methodology
can be used to automatically query satellite image providers and
download example imagery for a given area of interest and time interval,
using a configuration-driven approach.

## Notes on reproducibility

This replication package is designed to reproduce a single example run
of the data acquisition workflow.

The execution relies exclusively on the configuration file provided in `replication/config` directory and does not require manual interaction once started.
The example is intended to illustrate the behavior of the pipeline and
the structure of the generated outputs, rather than to provide a
complete or exhaustive dataset.

The provided configuration ensures that the example can be executed
without requiring additional input files beyond those included in the
replication package.

## Requirements

The replication package was tested with:

- Python >= 3.9
- Linux / macOS

All required Python dependencies are listed in `requirements.txt`.

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

## How to run the example

From the `replication/` directory, run:

```bash
python run_example.py
```
This command executes the data acquisition pipeline using the example
configuration file, performing the following steps:
- initialization of the data acquisition workflow
- querying of the configured satellite image providers
- retrieval and storage of metadata and downloadable products

## Expected output

After successful execution, the following outputs are generated:

- downloaded satellite images `replication/data/output` directory


## Citation

If you use this software or the replication package, please cite the
associated paper.