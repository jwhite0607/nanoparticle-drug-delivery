import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from model_v3 import simulate_calibrated_release


def metrics(actual, predicted):

    actual = np.asarray(actual)
    predicted = np.asarray(predicted)

    error = actual - predicted

    rmse = np.sqrt(np.mean(error ** 2))
    mae = np.mean(np.abs(error))

    ss_res = np.sum(error ** 2)
    ss_tot = np.sum(
        (actual - np.mean(actual)) ** 2
    )

    r2 = 1 - ss_res / ss_tot

    return rmse, mae, r2


def main():

    data = pd.read_csv(
        "experimental_data.csv"
    )

    experimental_time = data[
        "time_hours"
    ].values

    experimental_release = data[
        "experimental_release_percent"
    ].values

    radius = 200
    temperature = 37
    pH = 7.4
    degradation_rate = 0.005

    # Test diffusion scaling factors
    diffusion_scales = np.linspace(
        0.01,
        1.00,
        100
    )

    results = []

    for scale in diffusion_scales:

        model_time, model_release = (
            simulate_calibrated_release(
                radius_nm=radius,
                temperature_celsius=temperature,
                pH=pH,
                degradation_rate_per_hour=(
                    degradation_rate
                ),
                diffusion_scale=scale,
                total_time_hours=100
            )
        )

        predicted = np.interp(
            experimental_time,
            model_time,
            model_release
        )

        rmse, mae, r2 = metrics(
            experimental_release,
            predicted
        )

        results.append({
            "diffusion_scale": scale,
            "RMSE": rmse,
            "MAE": mae,
            "R_squared": r2
        })

    results_df = pd.DataFrame(results)

    best = results_df.loc[
        results_df["RMSE"].idxmin()
    ]

    print("=" * 65)
    print("VERSION 3 — DIFFUSION CALIBRATION")
    print("=" * 65)

    print(
        f"Best diffusion scale: "
        f"{best['diffusion_scale']:.4f}"
    )

    print(
        f"RMSE: {best['RMSE']:.3f}"
    )

    print(
        f"MAE: {best['MAE']:.3f}"
    )

    print(
        f"R²: {best['R_squared']:.4f}"
    )

    results_df.to_csv(
        "diffusion_optimization_results.csv",
        index=False
    )

    # Best model
    best_time, best_release = (
        simulate_calibrated_release(
            radius_nm=radius,
            temperature_celsius=temperature,
            pH=pH,
            degradation_rate_per_hour=(
                degradation_rate
            ),
            diffusion_scale=(
                best["diffusion_scale"]
            ),
            total_time_hours=100
        )
    )

    predicted = np.interp(
        experimental_time,
        best_time,
        best_release
    )

    comparison = pd.DataFrame({
        "time_hours": experimental_time,
        "experimental_release_percent":
            experimental_release,
        "v3_predicted_release_percent":
            predicted,
        "absolute_error_percent":
            np.abs(
                experimental_release - predicted
            )
    })

    print()
    print(comparison.to_string(index=False))

    comparison.to_csv(
        "validation_v3_results.csv",
        index=False
    )

    # Model comparison graph
    plt.figure(figsize=(10, 6))

    plt.scatter(
        experimental_time,
        experimental_release,
        s=70,
        label="Experimental data"
    )

    plt.plot(
        best_time,
        best_release,
        linewidth=2,
        label="Version 3 calibrated model"
    )

    plt.xlabel("Time (hours)")
    plt.ylabel(
        "Cumulative Drug Release (%)"
    )

    plt.title(
        "Experimental vs Calibrated Model"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "experimental_vs_model_v3.png",
        dpi=300
    )

    plt.show()

    # Optimization graph
    plt.figure(figsize=(10, 6))

    plt.plot(
        results_df["diffusion_scale"],
        results_df["RMSE"],
        marker="o",
        markersize=3
    )

    plt.xlabel(
        "Diffusion Scaling Factor"
    )

    plt.ylabel(
        "RMSE (percentage points)"
    )

    plt.title(
        "Diffusion Parameter Calibration"
    )

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "diffusion_calibration.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()