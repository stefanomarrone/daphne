<h1 align="center">DAPHNE
  <br/>
  <sub>Data Acquisition Pipeline for Heterogeneous Earth-observatioN sourcEs</sub>
</h1>

<p align="center">
  <a href="https://python.org"><img alt="Python" src="https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white"></a>
  <img alt="OS" src="https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Windows-informational">
  <a href="https://github.com/stefanomarrone/daphne/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/stefanomarrone/daphne?style=social"></a>
</p>

<p align="center">
  <img src="legacy_code/Figures/daphne_pipeline.png" alt="DAPHNE Pipeline Workflow" width="65%">
</p>

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

## Prerequisites and Environment Variables

Daphne may use serval external services to search and download satellite images: in these cases extra information could be added to the framework.
As example, if you want to use Google Earth Engine as an image provider, please add a _.env_ file to the project with the variable EARTHENGINE_PROJECT set to the name of the project on Google.

Here, some external providers are reported, with the environment variable to set:
* [Google Earth Engine](https://earthengine.google.com/): 
  * EARTHENGINE_PROJECT must be set to define the project.
* [OpenWeather](https://openweathermap.org): 
  * OPENWEATHER_API_KEY must be set to the generated token


## Dependencies
The framework is implemented in Python (version 3.9 recommended).

All required dependencies are listed in the `requirements.txt` file provided in the repository and can be installed using:

```bash
pip install -r requirements.txt
```
### Google Earth Engine prerequisite

Some acquisition scenarios supported by DAPHNE rely on **Google Earth Engine (GEE)** (e.g. MODIS or Landsat collections).

Due to Google Earth Engine access policies, running these scenarios requires
an **active Google Cloud project** associated with the user account.

To enable GEE-based acquisition, the user must:

1. Create or select a Google Cloud project, in the [Google Cloud Console](https://cloud.google.com/cloud-console?utm_source=google&utm_medium=cpc&utm_campaign=Cloud-SS-DR-GCP-1713666-GCP-DR-EMEA-IT-en-Google-BKWS-MIX-na&utm_content=c-Hybrid+%7C+BKWS+-+MIX+%7C+Txt+-+Generic+Cloud-Console-Cloud+Console-55675752867&utm_term=google+cloud+console&gclsrc=aw.ds&gad_source=1&gad_campaignid=19865870602&gclid=Cj0KCQiAnJHMBhDAARIsABr7b85HIhB9esBDoQl_FODAtKL7qTz8kGskge5fz6LI-vzAtymm5lhm1jAaAqKCEALw_wcB).
2. Define the project identifier locally as an environment variable.

In particular, the following variable must be added to the `.env` file:

```bash
EARTHENGINE_PROJECT=your_project_id
```
---

## Execution

Daphne depends on the MongoDB Service which can be downloaded and executed from https://github.com/stefanomarrone/mongodb_service

For the execution of Daphne, these steps are to follow:
1) Start MongoDB (external service)  
execute an instance of [MongoDB Service](https://github.com/stefanomarrone/mongodb_service) and take note of:
   - MongoDB IP address (e.g., `127.0.0.1`)
   - MongoDB port (e.g., `1813`) 
2) Start the DAPHNE API  
run the Daphne service with
```bash
python api_main.py <port_number> >mongodb_service_ip_address> <mongodb_service_port_number>  
```
3) Now you can request to DAPHNE a set of image/data retrivals by invoking the API _/execute_ endpoint
posting on that endpoint the items to request. The stucture of the JSON files are represented in [models.py](src/models.py) as a set of Pydantic classes.

4) After the response by DAPHNE, a JSON response is given back including the names of the retrieved files, which are stored by the Mongo Service.

An example of a simple client is in the Replication Package.

Note: Some providers (e.g. Google Earth Engine) require external credentials
and are therefore disabled by default unless explicitly configured.

---

## Replication Package

This repository includes a minimal replication package designed to reproduce
a representative data acquisition workflow using *DAPHNE*. See [README.md](replication/README.md). 

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

