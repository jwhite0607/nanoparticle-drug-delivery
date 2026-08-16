# Nanoparticle Drug Delivery Modeling & Optimization

## Overview

This project develops a computational engineering model for predicting controlled drug release from polymeric nanoparticles.

The model investigates how nanoparticle properties and environmental conditions influence drug-release behavior through mathematical modeling, calibration, validation, sensitivity analysis, and optimization.

## Engineering Objectives

The project investigates:

1. How nanoparticle radius affects drug-release time
2. How temperature affects drug release
3. How environmental pH affects release
4. How polymer degradation affects release
5. How accurately the model reproduces experimental data
6. What parameter combination minimizes model error

## Model Parameters

- Nanoparticle radius
- Temperature
- Environmental pH
- Polymer degradation rate

## Model Development

### Version 1

Initial nanoparticle drug-release model developed from the governing relationships between diffusion, environmental conditions, and polymer degradation.

### Version 2

The model was refined to improve the representation of the initial burst-release behavior and overall release profile.

### Version 3

The final model incorporated calibration against experimental data and produced substantially improved predictive agreement.

## Final Model Performance

The calibrated Version 3 model achieved:

| Metric | Result |
|---|---:|
| RMSE | 7.144 percentage points |
| MAE | 4.452 percentage points |
| R² | 0.9610 |
## Final Model Performance

| Metric | Result |
|---|---:|
| RMSE | 7.144 percentage points |
| MAE | 4.452 percentage points |
| R² | 0.9610 |

## Experimental Validation

### Experimental Data vs. Version 3 Model

The calibrated Version 3 model was compared against experimental drug-release measurements. The final model achieved an R² of 0.9610.

![Experimental vs Version 3 Model](experimental_vs_model_v3.png)

## Sensitivity Analysis

### Nanoparticle Radius

![Sensitivity to Nanoparticle Radius](sensitivity_v3_radius.png)

Larger nanoparticle radius results in longer predicted release times.

### Temperature

![Sensitivity to Temperature](sensitivity_v3_temperature.png)

Increasing temperature decreases predicted release time.

### Environmental pH

![Sensitivity to Environmental pH](sensitivity_v3_pH.png)

Increasing environmental pH decreases predicted release time.

### Polymer Degradation

![Sensitivity to Polymer Degradation](sensitivity_v3_degradation.png)

Increasing polymer degradation rate decreases predicted release time.
An R² of 0.9610 indicates a strong agreement between the calibrated model and the available experimental release data.

## Experimental Validation

The model was evaluated against experimental measurements at:

- 0 hours
- 1 hour
- 24 hours
- 48 hours
- 72 hours

The Version 3 model substantially improved agreement with the experimental release profile compared with earlier model versions.

## Optimization

The optimization analysis identified the following lowest-error configuration:

| Parameter | Optimized Value |
|---|---:|
| Nanoparticle radius | 200 nm |
| Temperature | 30 °C |
| Environmental pH | 7.0 |
| Polymer degradation rate | 0.005 1/hour |
| Predicted t50 | 13.83 hours |
| Predicted t90 | 35.07 hours |
| Optimization error | 4.205 |

## Sensitivity Analysis

The final model evaluates sensitivity to four major parameters.

### Nanoparticle Radius

Increasing nanoparticle radius increases predicted drug-release time, with larger particles generally producing slower release.

### Temperature

Increasing temperature decreases predicted release time, indicating faster release under the modeled conditions.

### Environmental pH

Increasing environmental pH decreases predicted release time within the modeled range.

### Polymer Degradation

Increasing polymer degradation rate decreases predicted release time because faster polymer degradation accelerates drug release.

## Key Results

The model demonstrates that:

- Nanoparticle size strongly influences release kinetics.
- Temperature affects the rate of release.
- Environmental pH significantly changes predicted release timing.
- Polymer degradation rate influences both t50 and t90.
- Model calibration substantially improves agreement with experimental data.
- The optimized configuration produced the lowest modeled error among the evaluated parameter combinations.

## Project Structure

```text
nanoparticle-drug-delivery/
│
├── main.py
├── model.py
├── model_v2.py
├── model_v3.py
├── optimization.py
├── sensitivity.py
├── sensitivity_v3.py
├── final_results_summary.py
│
├── experimental_data.csv
├── validation_results.csv
├── validation_v2_results.csv
├── validation_v3_results.csv
├── optimization_results.csv
│
├── sensitivity_v3_radius.csv
├── sensitivity_v3_temperature.csv
├── sensitivity_v3_pH.csv
├── sensitivity_v3_degradation.csv
│
├── experimental_vs_model.png
├── experimental_vs_model_v2.png
├── experimental_vs_model_v3.png
├── sensitivity_v3_radius.png
├── sensitivity_v3_temperature.png
├── sensitivity_v3_pH.png
├── sensitivity_v3_degradation.png
│
└── FINAL_REPORT.md