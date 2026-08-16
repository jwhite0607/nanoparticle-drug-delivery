import numpy as np
import matplotlib.pyplot as plt

from model import (
    diffusion_coefficient_temperature,
    pH_diffusion_factor,
    simulate_degrading_nanoparticle
)


def calculate_t50_t90(time, release):
    """
    Calculate the approximate time required
    to reach 50% and 90% drug release.
    """

    t50_index = np.abs(
        release - 50
    ).argmin()

    t90_index = np.abs(
        release - 90
    ).argmin()

    t50 = time[t50_index]
    t90 = time[t90_index]

    return t50, t90


def run_simulation(
    radius,
    temperature,
    pH,
    degradation_rate_per_hour
):
    """
    Run one complete simulation using
    radius, temperature, pH, and degradation.
    """

    # -----------------------------------------
    # Base model parameters
    # -----------------------------------------

    D0 = 3e-16

    activation_energy = 25000

    pKa = 6.5

    maximum_pH_factor = 5.0

    maximum_degradation_increase = 4.0

    # -----------------------------------------
    # Temperature effect
    # -----------------------------------------

    D_temperature = (
        diffusion_coefficient_temperature(
            temperature_celsius=temperature,
            D0=D0,
            activation_energy=activation_energy
        )
    )

    # -----------------------------------------
    # pH effect
    # -----------------------------------------

    pH_factor = pH_diffusion_factor(
        pH=pH,
        pKa=pKa,
        maximum_factor=maximum_pH_factor
    )

    # Effective initial diffusion
    initial_D = (
        D_temperature
        * pH_factor
    )

    # -----------------------------------------
    # Convert degradation rate
    # -----------------------------------------

    degradation_rate = (
        degradation_rate_per_hour
        / 3600
    )

    # -----------------------------------------
    # Run diffusion/degradation model
    # -----------------------------------------

    time, release = (
        simulate_degrading_nanoparticle(
            radius_nm=radius,
            initial_diffusion_coefficient=initial_D,
            degradation_rate=degradation_rate,
            maximum_degradation_increase=(
                maximum_degradation_increase
            ),
            total_time_hours=100
        )
    )

    return time, release


def sensitivity_analysis():
    """
    Run sensitivity analysis for each major parameter.
    """

    # -----------------------------------------
    # Baseline
    # -----------------------------------------

    baseline_radius = 200
    baseline_temperature = 37
    baseline_pH = 7.4
    baseline_degradation = 0.02

    print("=" * 60)
    print("NANOPARTICLE DRUG RELEASE SENSITIVITY ANALYSIS")
    print("=" * 60)

    # -----------------------------------------
    # Radius sensitivity
    # -----------------------------------------

    radii = [
        50,
        100,
        200,
        300,
        500
    ]

    radius_t50 = []
    radius_t90 = []

    for radius in radii:

        time, release = run_simulation(
            radius=radius,
            temperature=baseline_temperature,
            pH=baseline_pH,
            degradation_rate_per_hour=(
                baseline_degradation
            )
        )

        t50, t90 = calculate_t50_t90(
            time,
            release
        )

        radius_t50.append(t50)
        radius_t90.append(t90)

    # -----------------------------------------
    # Temperature sensitivity
    # -----------------------------------------

    temperatures = [
        20,
        25,
        30,
        37,
        40,
        45
    ]

    temperature_t50 = []
    temperature_t90 = []

    for temperature in temperatures:

        time, release = run_simulation(
            radius=baseline_radius,
            temperature=temperature,
            pH=baseline_pH,
            degradation_rate_per_hour=(
                baseline_degradation
            )
        )

        t50, t90 = calculate_t50_t90(
            time,
            release
        )

        temperature_t50.append(t50)
        temperature_t90.append(t90)

    # -----------------------------------------
    # pH sensitivity
    # -----------------------------------------

    pH_values = [
        5.0,
        5.5,
        6.0,
        6.5,
        7.0,
        7.4,
        8.0
    ]

    pH_t50 = []
    pH_t90 = []

    for pH in pH_values:

        time, release = run_simulation(
            radius=baseline_radius,
            temperature=baseline_temperature,
            pH=pH,
            degradation_rate_per_hour=(
                baseline_degradation
            )
        )

        t50, t90 = calculate_t50_t90(
            time,
            release
        )

        pH_t50.append(t50)
        pH_t90.append(t90)

    # -----------------------------------------
    # Degradation sensitivity
    # -----------------------------------------

    degradation_rates = [
        0.005,
        0.01,
        0.02,
        0.03,
        0.05
    ]

    degradation_t50 = []
    degradation_t90 = []

    for degradation in degradation_rates:

        time, release = run_simulation(
            radius=baseline_radius,
            temperature=baseline_temperature,
            pH=baseline_pH,
            degradation_rate_per_hour=degradation
        )

        t50, t90 = calculate_t50_t90(
            time,
            release
        )

        degradation_t50.append(t50)
        degradation_t90.append(t90)

    # -----------------------------------------
    # Print results
    # -----------------------------------------

    print("\nRADIUS")
    print("-" * 60)

    for r, t50, t90 in zip(
        radii,
        radius_t50,
        radius_t90
    ):

        print(
            f"{r:>5} nm | "
            f"t50 = {t50:6.2f} hr | "
            f"t90 = {t90:6.2f} hr"
        )

    print("\nTEMPERATURE")
    print("-" * 60)

    for temp, t50, t90 in zip(
        temperatures,
        temperature_t50,
        temperature_t90
    ):

        print(
            f"{temp:>5} °C | "
            f"t50 = {t50:6.2f} hr | "
            f"t90 = {t90:6.2f} hr"
        )

    print("\nPH")
    print("-" * 60)

    for pH, t50, t90 in zip(
        pH_values,
        pH_t50,
        pH_t90
    ):

        print(
            f"{pH:>5.1f} | "
            f"t50 = {t50:6.2f} hr | "
            f"t90 = {t90:6.2f} hr"
        )

    print("\nPOLYMER DEGRADATION")
    print("-" * 60)

    for rate, t50, t90 in zip(
        degradation_rates,
        degradation_t50,
        degradation_t90
    ):

        print(
            f"{rate:>5.3f} 1/hr | "
            f"t50 = {t50:6.2f} hr | "
            f"t90 = {t90:6.2f} hr"
        )

    # -----------------------------------------
    # Create figures
    # -----------------------------------------

    # Radius
    plt.figure(figsize=(9, 6))

    plt.plot(
        radii,
        radius_t50,
        marker="o",
        label="t50"
    )

    plt.plot(
        radii,
        radius_t90,
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
        "Sensitivity to Nanoparticle Radius"
    )

    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "sensitivity_radius.png",
        dpi=300
    )

    plt.show()

    # Temperature
    plt.figure(figsize=(9, 6))

    plt.plot(
        temperatures,
        temperature_t50,
        marker="o",
        label="t50"
    )

    plt.plot(
        temperatures,
        temperature_t90,
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
        "Sensitivity to Temperature"
    )

    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "sensitivity_temperature.png",
        dpi=300
    )

    plt.show()

    # pH
    plt.figure(figsize=(9, 6))

    plt.plot(
        pH_values,
        pH_t50,
        marker="o",
        label="t50"
    )

    plt.plot(
        pH_values,
        pH_t90,
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
        "Sensitivity to Environmental pH"
    )

    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "sensitivity_pH.png",
        dpi=300
    )

    plt.show()

    # Degradation
    plt.figure(figsize=(9, 6))

    plt.plot(
        degradation_rates,
        degradation_t50,
        marker="o",
        label="t50"
    )

    plt.plot(
        degradation_rates,
        degradation_t90,
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
        "Sensitivity to Polymer Degradation"
    )

    plt.grid(True, alpha=0.3)

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "sensitivity_degradation.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    sensitivity_analysis()