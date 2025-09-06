# Bachelor Thesis – Falling Through the System  

you can find the thesis [here](thesis.pdf)

**Quantitative Visualization of Patient Pathways Surrounding Inpatient Falls**

This repository contains the code, notebooks, and supporting files for my bachelor thesis submitted at Technische Universität Berlin, titled *“Falling Through the System: Quantitative Visualization of Patient Pathways Surrounding Inpatient Falls”*.  

The thesis investigates inpatient falls in a German university hospital (2016–2022) using quantitative health analytics. The research focuses on two central questions:  

1. **How do the incidence and characteristics of inpatient falls vary across clinical departments?**  
2. **How do patient pathways of those who experience falls differ across departments?**  

The analysis builds on electronic health records (EHR) to examine demographic patterns, injury severity, temporal fall distributions, and department-level variations. Furthermore, a **Fall Vulnerability Score (FVS)** is developed to rank departments by fall risk. Finally, patient pathways leading to severe fall-related injuries are visualized with Sankey diagrams to identify structural vulnerabilities.

---

## Repository Structure

The repository is organized to reflect the workflow of the thesis: from data preparation, to descriptive statistics, to visualization of patient pathways.  

### 1. Data Preparation
- [**00_specialities_prep.ipynb**](00_specialities_prep.ipynb)  
  Maps hospital wards to departments using cost center information and prepares a consistent dataset for analysis.

- [**99_spec_adjsustment.ipynb**](99_spec_adjsustment.ipynb)  
  Contains late-stage adjustments and refinements to the specialties/departments mapping for better consistency in downstream analysis.

### 2. Initial Data Load
- [**01_initial_load.ipynb**](01_initial_load.ipynb)  
  Handles the loading and preprocessing of pseudonymized hospital EHR data. Filters movements, patient cases, and fall documentation to the relevant timeframe (2016–2022). Ensures data validity and produces the cleaned dataset used in subsequent steps.

### 3. Descriptive Analysis (Research Question 1)
- [**02_Q_01.ipynb**](02_Q_01.ipynb)  
  Descriptive analysis of inpatient falls across departments:  
  - Fall incidence rates (per 1,000 patient days)  
  - Age and gender distribution of fallers  
  - Fall timing across shifts  
  - Injury severity patterns  
  - Construction of the **Fall Vulnerability Score (FVS)**

- [**Q_01.md**](Q_01.md)  
  Markdown documentation summarizing the results, interpretations, and visual outputs from the descriptive analysis.

### 4. Patient Pathway Analysis (Research Question 2)
- [**03_Q_02.ipynb**](03_Q_02.ipynb)  
  Builds patient pathways for those who suffered falls in the most vulnerable departments (as identified by the FVS). Implements filtering by injury severity and alignment around fall events. Generates data structures for pathway visualization.

- [**05_Q_02_graph_mover.py**](05_Q_02_graph_mover.py)  
  Helper script for constructing Sankey diagrams and handling movement data between departments. Implements transformations such as interval merging and summary events for pathway simplification.

- [**q2_helper.py**](q2_helper.py)  
  Utility functions supporting patient pathway extraction and preprocessing (e.g., filtering, alignment, marker insertion).

---


---

## Data Privacy and Ethics  
This project strictly adheres to data privacy regulations. All patient data was pseudonymized before analysis, and any potentially identifying information has been removed or generalized. The analysis is conducted in compliance with ethical standards for handling sensitive health data.

Furthermore, this repository does not contain any raw data files. The notebooks are designed to be run in an environment where the appropriate pseudonymized datasets are available, ensuring that no sensitive information is exposed.


## Thesis Reference
Jakob Micha Möhler (2024). *Falling Through the System: Quantitative Visualization of Patient Pathways Surrounding Inpatient Falls*. Bachelor’s Thesis, Technische Universität Berlin.  
