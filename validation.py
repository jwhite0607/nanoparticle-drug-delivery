import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sensitivity import run_simulation


def calculate_metrics(experimental, predicted):
    """Calculate model-validation metrics."""

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

    mean_percentage_error = np.mean(
        np.abs(error)
        / np.maximum(experimental, 1e-8)
    ) * 100

    return (
        rmse,
        mae,
        r_squared,
        mean_percentage_error
    )


def main():

    print("=" * 70)
    print("NANOPARTICLE DRUG-RELEASE MODEL VALIDATION")
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

    # Start with the optimized degradation rate
    degradation_rate = 0.005

    # --------------------------------------------------
    # Run model
    # --------------------------------------------------

    model_time, model_release = run_simulation(
        radius=radius,
        temperature=temperature,
        pH=pH,
        degradation_rate_per_hour=degradation_rate
    )

    # --------------------------------------------------
    # Interpolate model at experimental times
    # --------------------------------------------------

    predicted_release = np.interp(
        experimental_time,
        model_time,
        model_release
    )

    # --------------------------------------------------
    # Calculate metrics
    # --------------------------------------------------

    (
        rmse,
        mae,
        r_squared,
        percentage_error
    ) = calculate_metrics(
        experimental_release,
        predicted_release
    )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print()
    print("EXPERIMENTAL CONDITIONS")
    print("-" * 70)

    print(f"Nanoparticle radius: {radius} nm")
    print(f"Temperature: {temperature} °C")
    print(f"pH: {pH}")
    print(
        f"Degradation rate: "
        f"{degradation_rate} 1/hour"
    )

    print()
    print("VALIDATION RESULTS")
    print("-" * 70)

    print(
        f"RMSE: "
        f"{rmse:.3f} percentage points"
    )

    print(
        f"MAE: "
        f"{mae:.3f} percentage points"
    )

    print(
        f"R²: "
        f"{r_squared:.4f}"
    )

    print(
        f"Mean absolute percentage error: "
        f"{percentage_error:.2f}%"
    )

    # --------------------------------------------------
    # Comparison table
    # --------------------------------------------------

    comparison = pd.DataFrame({
        "time_hours": experimental_time,
        "experimental_release_percent": (
            experimental_release
        ),
        "predicted_release_percent": (
            predicted_release
        ),
        "absolute_error_percent": np.abs(
            experimental_release
            - predicted_release
        )
    })

    print()
    print("EXPERIMENTAL VS MODEL")
    print("-" * 70)

    print(
        comparison.to_string(
            index=False
        )
    )

    comparison.to_csv(
        "validation_results.csv",
        index=False
    )

    # --------------------------------------------------
    # Plot
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
        model_time,
        model_release,
        linewidth=2,
        label="Model prediction"
    )

    plt.xlabel(
        "Time (hours)"
    )

    plt.ylabel(
        "Cumulative Drug Release (%)"
    )

    plt.title(
        "Experimental vs Model Drug Release"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "experimental_vs_model.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()