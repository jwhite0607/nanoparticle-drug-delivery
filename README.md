# Nanoparticle Drug Delivery Modeling & Optimization

## Overview

This project develops a computational model for predicting controlled drug release from polymeric nanoparticles.

The model investigates how nanoparticle properties and environmental conditions affect drug-release behavior and uses calibration, sensitivity analysis, validation, and optimization to identify favorable operating conditions.

## Engineering Questions

The project investigates:

1. How does nanoparticle radius affect drug-release time?
2. How does temperature affect drug release?
3. How does environmental pH affect release?
4. How does polymer degradation affect release?
5. How accurately can the model reproduce experimental data?
6. What combination of parameters produces the lowest model error?

## Model Parameters

- Nanoparticle radius
- Temperature
- Environmental pH
- Polymer degradation rate

## Final Model Performance

The calibrated Version 3 model achieved:

| Metric | Result |
|---|---:|
| RMSE | 7.144 percentage points |
| MAE | 4.452 percentage points |
| R² | 0.9610 |

## Optimized Configuration

| Parameter | Value |
|---|---:|
| Radius | 200 nm |
| Temperature | 30 °C |
| pH | 7.0 |
| Degradation rate | 0.005 1/hour |
| Predicted t50 | 13.83 hours |
| Predicted t90 | 35.07 hours |
| Optimization error | 4.205 |

## Sensitivity Analysis

The final model includes sensitivity analyses for:

- Nanoparticle radius
- Temperature
- Environmental pH
- Polymer degradation rate

These analyses demonstrate how changes in each parameter affect predicted drug-release timing.

## Validation

The model was compared against experimental measurements at:

- 0 hours
- 1 hour
- 24 hours
- 48 hours
- 72 hours

The calibrated Version 3 model substantially improved agreement with the experimental release profile.

## Project Outputs

### Figures

- `sensitivity_v3_radius.png`
- `sensitivity_v3_temperature.png`
- `sensitivity_v3_pH.png`
- `sensitivity_v3_degradation.png`

### Data

- `experimental_data.csv`
- `validation_v3_results.csv`
- `optimization_results.csv`
- `sensitivity_v3_radius.csv`
- `sensitivity_v3_temperature.csv`
- `sensitivity_v3_pH.csv`
- `sensitivity_v3_degradation.csv`

## Limitations

This is a computational engineering model and does not constitute experimental or clinical validation. Additional experimental data would be required to establish broader predictive reliability.

## Conclusion

The project demonstrates the use of computational modeling, calibration, validation, sensitivity analysis, and optimization to investigate controlled nanoparticle drug release.

The Version 3 model achieved an R² of 0.9610 against the available experimental data and identified a lowest-error configuration of 200 nm radius, 30 °C, pH 7.0, and a polymer degradation rate of 0.005 1/hour.