# Replication Package
The goal is to demonstrate how the framework can be configured and executed to retrieve satellite imagery.  

The goal of this package is to demonstrate how the proposed methodology
can be used to automatically query satellite image providers and
download example imagery for a given area of interest and time interval,
using a configuration-driven approach.

### Included materials

This directory provides a minimal and self-contained replication package
to reproduce an example run of the data acquisition pipeline implemented
in the DAPHNE module. The replication package provides:

- a sample configuration file defining;
- a minimal execution example using open-access data sources; **TODO**
- a reproducible directory structure for downloaded data. **TODO**

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

First start MongoService with the config.ini paremeters (see [https://github.com/stefanomarrone/mongodb_service](https://github.com/stefanomarrone/mongodb_service)).

Then start DAPHNE with 
```bash
python api_main.py 1813 127.0.0.1 1812
```

From the `replication/` directory, run:

```bash
python replication_package.py
```

This command executes the data acquisition pipeline using the example
configuration file, performing the following steps:
- initialization of the data acquisition workflow
- querying of the configured satellite image providers
- retrieval and storage of metadata and downloadable products

## Expected output
After successful execution, you can see the output on Mongo Service. Furthremore, the local outputs are generated in the [./output](./output) folder.
