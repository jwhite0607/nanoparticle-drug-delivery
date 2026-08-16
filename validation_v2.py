import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from model_v2 import simulate_burst_release


def calculate_metrics(experimental, predicted):
    experimental = np.asarray(experimental)
    predicted = np.asarray(predicted)

    error = experimental - predicted

    rmse = np.sqrt(
        np.mean(error ** 2)
    )

    mae = np.mean(
        np.abs(error)
    )

    ss_res = np.sum(
        (experimental - predicted) ** 2
    )

    ss_tot = np.sum(
        (experimental - np.mean(experimental)) ** 2
    )

    r_squared = (
        1 - ss_res / ss_tot
    )

    return rmse, mae, r_squared


def main():

    print("=" * 70)
    print("VERSION 2 MODEL VALIDATION")
    print("=" * 70)

    # --------------------------------------------------
    # Load experimental data
    # --------------------------------------------------

    data = pd.read_csv(
        "experimental_data.csv"
    )

    experimental_time = (
        data["time_hours"].values
    )

    experimental_release = (
        data["experimental_release_percent"].values
    )

    # --------------------------------------------------
    # Experimental conditions
    # --------------------------------------------------

    radius = 200
    temperature = 37
    pH = 7.4
    degradation_rate = 0.005

    # --------------------------------------------------
    # Test burst fractions
    # --------------------------------------------------

    burst_fractions = np.arange(
        0.05,
        0.41,
        0.01
    )

    results = []

    best_result = None

    print()
    print(
        f"Testing {len(burst_fractions)} "
        "burst fractions..."
    )

    for burst_fraction in burst_fractions:

        model_time, model_release = (
            simulate_burst_release(
                radius_nm=radius,
                temperature_celsius=temperature,
                pH=pH,
                degradation_rate_per_hour=(
                    degradation_rate
                ),
                burst_fraction=burst_fraction,
                total_time_hours=100
            )
        )

        predicted_release = np.interp(
            experimental_time,
            model_time,
            model_release
        )

        rmse, mae, r_squared = (
            calculate_metrics(
                experimental_release,
                predicted_release
            )
        )

        results.append({
            "burst_fraction": burst_fraction,
            "burst_percent": burst_fraction * 100,
            "RMSE": rmse,
            "MAE": mae,
            "R_squared": r_squared
        })

        if (
            best_result is None
            or rmse < best_result["RMSE"]
        ):

            best_result = {
                "burst_fraction": burst_fraction,
                "burst_percent": burst_fraction * 100,
                "RMSE": rmse,
                "MAE": mae,
                "R_squared": r_squared
            }

    # --------------------------------------------------
    # Save results
    # --------------------------------------------------

    results_df = pd.DataFrame(
        results
    )

    results_df = results_df.sort_values(
        by="RMSE"
    )

    results_df.to_csv(
        "burst_optimization_results.csv",
        index=False
    )

    # --------------------------------------------------
    # Print best result
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("BEST BURST FRACTION")
    print("=" * 70)

    print(
        f"Burst fraction: "
        f"{best_result['burst_fraction']:.2f}"
    )

    print(
        f"Initial burst: "
        f"{best_result['burst_percent']:.2f}%"
    )

    print(
        f"RMSE: "
        f"{best_result['RMSE']:.3f}"
    )

    print(
        f"MAE: "
        f"{best_result['MAE']:.3f}"
    )

    print(
        f"R²: "
        f"{best_result['R_squared']:.4f}"
    )

    # --------------------------------------------------
    # Best model prediction
    # --------------------------------------------------

    best_time, best_release = (
        simulate_burst_release(
            radius_nm=radius,
            temperature_celsius=temperature,
            pH=pH,
            degradation_rate_per_hour=(
                degradation_rate
            ),
            burst_fraction=(
                best_result["burst_fraction"]
            ),
            total_time_hours=100
        )
    )

    predicted_release = np.interp(
        experimental_time,
        best_time,
        best_release
    )

    # --------------------------------------------------
    # Comparison table
    # --------------------------------------------------

    comparison = pd.DataFrame({
        "time_hours": experimental_time,
        "experimental_release_percent": (
            experimental_release
        ),
        "v2_predicted_release_percent": (
            predicted_release
        ),
        "absolute_error_percent": np.abs(
            experimental_release
            - predicted_release
        )
    })

    print()
    print("=" * 70)
    print("VERSION 2 EXPERIMENTAL VS MODEL")
    print("=" * 70)

    print(
        comparison.to_string(
            index=False
        )
    )

    comparison.to_csv(
        "validation_v2_results.csv",
        index=False
    )

    # --------------------------------------------------
    # Plot V2
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.scatter(
        experimental_time,
        experimental_release,
        s=70,
        label="Experimental data",
        zorder=3
    )

    plt.plot(
        best_time,
        best_release,
        linewidth=2,
        label="Version 2 model"
    )

    plt.xlabel(
        "Time (hours)"
    )

    plt.ylabel(
        "Cumulative Drug Release (%)"
    )

    plt.title(
        "Version 2: Experimental vs Model"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "experimental_vs_model_v2.png",
        dpi=300
    )

    plt.show()

    # --------------------------------------------------
    # Plot burst optimization
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        results_df["burst_percent"],
        results_df["RMSE"],
        marker="o"
    )

    plt.xlabel(
        "Initial Burst Release (%)"
    )

    plt.ylabel(
        "RMSE (percentage points)"
    )

    plt.title(
        "Effect of Initial Burst Fraction on Model Error"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        "burst_fraction_optimization.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()