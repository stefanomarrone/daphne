<h1 align="center">DAPHNE
  <br/>
  <sub>Data Acquisition Pipeline for Heterogeneous Earth-observatioN sourcEs</sub>
</h1>

<p align="center">
  <a href="https://python.org"><img alt="Python" src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white"></a>
  <img alt="OS" src="https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Windows-informational">
  <a href="https://github.com/stefanomarrone/daphne/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/stefanomarrone/daphne?style=social"></a>
</p>

<!--
<p align="center">
  <img src="Figures/daphne_pipeline.png" alt="DAPHNE Pipeline Workflow" width="40%">
</p>
-->

**DAPHNE** is a modular data acquisition framework designed to retrieve satellite imagery and environmental data from heterogeneous sources through a unified and configurable interface.

The framework supports reproducible research workflows by abstracting provider-specific access mechanisms and offering a rule-based, configuration-driven approach to data collection.

**Relation to Other Projects**  
DAPHNE is the data acquisition component of the **TITANIA** framework, which integrates satellite data retrieval and vegetation pattern analysis within a unified architecture.
The data collected by DAPHNE can be directly processed by downstream modules such as **[SILVIA](https://github.com/Ste-lla02/silvia)** for image segmentation and analysis.

---

## Motivation

The growing availability of Earth Observation data from multiple open-access and commercial providers has significantly expanded research opportunities in environmental monitoring and geospatial analysis.  
However, data acquisition remains a major bottleneck due to:

- heterogeneous access protocols and APIs,
- provider-specific query languages and constraints,
- lack of uniform metadata and reproducibility,
- manual and error-prone data retrieval processes.

DAPHNE addresses these challenges by providing a unified framework for satellite and environmental data acquisition, enabling researchers to focus on downstream analysis rather than data access complexity.

---

## Main Features

- **Unified access to heterogeneous providers**  
  Support for multiple satellite imagery and environmental data sources through a single interface.

- **Configuration-driven acquisition**  
  Data retrieval is controlled via user-defined configuration files, ensuring reproducibility.

- **Rule-based provider selection**  
  Automatic selection of suitable data sources based on user constraints (e.g. resolution, time range, area of interest).

- **Reproducible data organisation**  
  Retrieved data are stored following a structured and traceable directory layout.

- **Research-oriented and extensible**  
  Designed to support experimentation and easy integration of new providers.

---

## Supported Data Sources

Depending on the configuration, DAPHNE can retrieve data from:
- open-access satellite catalogues (e.g. Copernicus, Landsat, MODIS),
- commercial satellite imagery providers,
- meteorological and environmental data services.

The list of supported providers can be extended as new APIs are integrated.

---

## Architecture Overview

DAPHNE acts as the data acquisition component within a modular research pipeline.  
It abstracts provider-specific logic behind a unified interface, enabling seamless integration with downstream processing and analysis modules.

---

## Dependencies

The framework is implemented in Python (version 3.9 recommended).

All required dependencies are listed in the `requirements.txt` file provided in the repository and can be installed using:

```bash
pip install -r requirements.txt
```

---
## License
The software is licensed according to the GNU General Public License v3.0 (see License file).

---
## Contact
For questions or collaborations:

**Maria Stella de Biase**  
University of Campania “Luigi Vanvitelli”  
📧 mariastella.debiase@unicampania.it

**Stefano Marrone**  
University of Campania “Luigi Vanvitelli”  
📧 stefano.marrone@unicampania.it

---

