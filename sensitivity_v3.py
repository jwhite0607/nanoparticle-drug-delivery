import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from model_v3 import simulate_calibrated_release


# --------------------------------------------------
# Calculate t50 and t90
# --------------------------------------------------

def release_times(time, release):

    time = np.asarray(time)
    release = np.asarray(release)

    # Find t50
    if release.max() >= 50:
        t50 = np.interp(50, release, time)
    else:
        t50 = np.nan

    # Find t90
    if release.max() >= 90:
        t90 = np.interp(90, release, time)
    else:
        t90 = np.nan

    return t50, t90

# --------------------------------------------------
# Run one simulation
# --------------------------------------------------

def run_model(
    radius,
    temperature,
    pH,
    degradation_rate,
    diffusion_scale
):

    time, release = simulate_calibrated_release(
        radius_nm=radius,
        temperature_celsius=temperature,
        pH=pH,
        degradation_rate_per_hour=degradation_rate,
        diffusion_scale=diffusion_scale,
        total_time_hours=500
    )

    return release_times(
        time,
        release
    )


def main():

    # --------------------------------------------------
    # Calibrated baseline
    # --------------------------------------------------

    radius = 200
    temperature = 37
    pH = 7.4
    degradation_rate = 0.005

    # IMPORTANT:
    # Replace this with the "Best diffusion scale"
    # printed by validation_v3.py
    diffusion_scale = 0.10

    # --------------------------------------------------
    # Radius sensitivity
    # --------------------------------------------------

    radii = [
        50,
        100,
        150,
        200,
        250,
        300,
        400,
        500
    ]

    radius_results = []

    for r in radii:

        t50, t90 = run_model(
            r,
            temperature,
            pH,
            degradation_rate,
            diffusion_scale
        )

        radius_results.append(
            [r, t50, t90]
        )

    radius_df = pd.DataFrame(
        radius_results,
        columns=[
            "radius_nm",
            "t50_hours",
            "t90_hours"
        ]
    )

    radius_df.to_csv(
        "sensitivity_v3_radius.csv",
        index=False
    )

    # --------------------------------------------------
    # Temperature sensitivity
    # --------------------------------------------------

    temperatures = [
        20,
        25,
        30,
        35,
        37,
        40,
        45
    ]

    temperature_results = []

    for temp in temperatures:

        t50, t90 = run_model(
            radius,
            temp,
            pH,
            degradation_rate,
            diffusion_scale
        )

        temperature_results.append(
            [temp, t50, t90]
        )

    temperature_df = pd.DataFrame(
        temperature_results,
        columns=[
            "temperature_celsius",
            "t50_hours",
            "t90_hours"
        ]
    )

    temperature_df.to_csv(
        "sensitivity_v3_temperature.csv",
        index=False
    )

    # --------------------------------------------------
    # pH sensitivity
    # --------------------------------------------------

    pH_values = [
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.4,
        8.0
    ]

    pH_results = []

    for ph in pH_values:

        t50, t90 = run_model(
            radius,
            temperature,
            ph,
            degradation_rate,
            diffusion_scale
        )

        pH_results.append(
            [ph, t50, t90]
        )

    pH_df = pd.DataFrame(
        pH_results,
        columns=[
            "pH",
            "t50_hours",
            "t90_hours"
        ]
    )

    pH_df.to_csv(
        "sensitivity_v3_pH.csv",
        index=False
    )

    # --------------------------------------------------
    # Polymer degradation sensitivity
    # --------------------------------------------------

    degradation_rates = [
        0.001,
        0.003,
        0.005,
        0.010,
        0.020,
        0.030,
        0.050
    ]

    degradation_results = []

    for rate in degradation_rates:

        t50, t90 = run_model(
            radius,
            temperature,
            pH,
            rate,
            diffusion_scale
        )

        degradation_results.append(
            [rate, t50, t90]
        )

    degradation_df = pd.DataFrame(
        degradation_results,
        columns=[
            "degradation_rate_per_hour",
            "t50_hours",
            "t90_hours"
        ]
    )

    degradation_df.to_csv(
        "sensitivity_v3_degradation.csv",
        index=False
    )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print()
    print("=" * 70)
    print("VERSION 3 SENSITIVITY ANALYSIS")
    print("=" * 70)

    print("\nRADIUS")
    print(radius_df.to_string(index=False))

    print("\nTEMPERATURE")
    print(temperature_df.to_string(index=False))

    print("\nPH")
    print(pH_df.to_string(index=False))

    print("\nPOLYMER DEGRADATION")
    print(
        degradation_df.to_string(index=False)
    )

    # --------------------------------------------------
    # Radius graph
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        radii,
        radius_df["t50_hours"],
        marker="o",
        label="t50"
    )

    plt.plot(
        radii,
        radius_df["t90_hours"],
        marker="s",
        label="t90"
    )

    plt.xlabel(
        "Nanoparticle Radius (nm)"
    )

    plt.ylabel(
        "Release Time (hours)"
    )

    plt.title(
        "Version 3 Sensitivity to Nanoparticle Radius"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "sensitivity_v3_radius.png",
        dpi=300
    )

    plt.show()

    # --------------------------------------------------
    # Temperature graph
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        temperatures,
        temperature_df["t50_hours"],
        marker="o",
        label="t50"
    )

    plt.plot(
        temperatures,
        temperature_df["t90_hours"],
        marker="s",
        label="t90"
    )

    plt.xlabel(
        "Temperature (°C)"
    )

    plt.ylabel(
        "Release Time (hours)"
    )

    plt.title(
        "Version 3 Sensitivity to Temperature"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "sensitivity_v3_temperature.png",
        dpi=300
    )

    plt.show()

    # --------------------------------------------------
    # pH graph
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        pH_values,
        pH_df["t50_hours"],
        marker="o",
        label="t50"
    )

    plt.plot(
        pH_values,
        pH_df["t90_hours"],
        marker="s",
        label="t90"
    )

    plt.xlabel(
        "Environmental pH"
    )

    plt.ylabel(
        "Release Time (hours)"
    )

    plt.title(
        "Version 3 Sensitivity to Environmental pH"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "sensitivity_v3_pH.png",
        dpi=300
    )

    plt.show()

    # --------------------------------------------------
    # Degradation graph
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        degradation_rates,
        degradation_df["t50_hours"],
        marker="o",
        label="t50"
    )

    plt.plot(
        degradation_rates,
        degradation_df["t90_hours"],
        marker="s",
        label="t90"
    )

    plt.xlabel(
        "Polymer Degradation Rate (1/hour)"
    )

    plt.ylabel(
        "Release Time (hours)"
    )

    plt.title(
        "Version 3 Sensitivity to Polymer Degradation"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "sensitivity_v3_degradation.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()