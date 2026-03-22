# Technical Architecture: NPCI Sentinel

## 1. Problem Philosophy
[cite_start]Insider threats originate from trusted individuals[cite: 4]. [cite_start]Sentinel focuses on **Behavioral DNA** rather than just signature-based detection.

## [cite_start]2. Dataset Processing Module 
- [cite_start]**Log Ingestion:** Processes structured email and system logs[cite: 24].
- [cite_start]**Feature Engineering:** Extracts temporal patterns (after-hours activity) and volume metrics.
- **Psychometric Correlation:** Merges activity logs with OCEAN scores to identify "Propensity for Risk" based on personality traits.

## [cite_start]3. Detection Engine 
[cite_start]We utilize a **Hybrid Two-Tier Ensemble**[cite: 56]:
- **Tier 1 (Isolation Forest):** Efficiently identifies global outliers and point anomalies in activity frequency.
- [cite_start]**Tier 2 (PyTorch Autoencoder):** A deep learning model that learns "Normal Behavior Sequences"[cite: 53]. High reconstruction error flags complex behavioral shifts.
- **Explainability:** SHAP (SHapley Additive exPlanations) decomposes the risk score into specific contributing factors (e.g., high attachment count).

## [cite_start]4. Privacy & Security [cite: 38, 64]
- [cite_start]**Anonymization:** SHA-256 Hashing of all User IDs and PII[cite: 39, 65].
- [cite_start]**Encryption:** AES-256 logic for secure data transmission[cite: 40, 66].