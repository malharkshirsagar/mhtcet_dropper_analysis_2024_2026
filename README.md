# MHT-CET Longitudinal Dropper Analysis (2024–2026)

An end-to-end data engineering pipeline and statistical analysis framework designed to evaluate score trajectories, percentile shifts, and performance trends of MHT-CET repeater (dropper) candidates across academic cycles.

---

# Project Overview

Analyzing multi-year government examination records presents significant data quality and structural challenges. This project builds a robust, automated Python pipeline to ingest, clean, cross-verify, and analyze longitudinal candidate records while adhering to strict data privacy standards.

### Key Highlights
* **Scale:** Processed and cross-verified **28,681 records** with **0 anomalies** post-validation.
* **Pipeline:** Built using Python and Pandas for high-performance tabular transformation and deterministic validation.
* **Privacy-First Design:** Raw static anchor columns (`SSC Total %`, `HSC %`, and candidate names) were fully decoupled and scrubbed prior to publication to prevent reverse-engineering or individual tracking.

---

##  Technical Architecture & Features

The project utilizes a strict **Static vs. Dynamic** feature classification strategy for entity resolution across multi-year state examination portals:

1. **Static Anchors (Immutable Baseline):**
   * Core academic background metrics (`SSC Total %`, subject-wise scores).
   * Demographic markers (`Category`, `Gender`).
2. **Dynamic Targets (Mutable Performance Metrics):**
   * Annual merit rankings (`Merit NO`, application identifiers).
   * Score-based performance outputs (`Percentile`, subject-wise percentile distributions).

---

# Data Privacy & Compliance
To ensure complete compliance with ethical data sharing standards:

1.All personally identifiable information (PII) including full names has been completely removed.

2.Bridge identifiers (such as foundational 10th/12th grade linkages) have been stripped from the published dataset to ensure individuals cannot be re-identified or reconstructed.

3.The underlying code framework remains fully open-source for analytical replication.

----
# License
This project is open-source and available under the terms of the MIT License.