import matplotlib.pyplot as plt

from model import (
    diffusion_coefficient_temperature,
    simulate_degrading_nanoparticle
)


def main():

    print("=" * 60)
    print("POLYMER DEGRADATION DRUG-RELEASE MODEL")
    print("=" * 60)

    # ------------------------------------------------
    # Nanoparticle properties
    # ------------------------------------------------

    radius = 200

    temperature = 37

    # ------------------------------------------------
    # Temperature-dependent diffusion parameters
    # ------------------------------------------------

    # Illustrative starting parameters.
    # These will later be replaced with
    # literature-derived values.

    D0 = 3e-16

    activation_energy = 25000

    # Calculate diffusion coefficient at 37 °C
    initial_D = diffusion_coefficient_temperature(
        temperature_celsius=temperature,
        D0=D0,
        activation_energy=activation_energy
    )

    print()
    print(
        f"Temperature: {temperature} °C"
    )

    print(
        f"Initial diffusion coefficient: "
        f"{initial_D:.3e} m²/s"
    )

    # ------------------------------------------------
    # Polymer degradation rates
    # ------------------------------------------------

    # These are rates in 1/hour.
    degradation_rates_per_hour = [
        0.005,
        0.010,
        0.020,
        0.050
    ]

    # Convert rates from 1/hour to 1/second
    degradation_rates = [
        rate / 3600
        for rate in degradation_rates_per_hour
    ]

    maximum_degradation_increase = 4.0

    # ------------------------------------------------
    # Plot
    # ------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    for rate_per_hour, degradation_rate in zip(
        degradation_rates_per_hour,
        degradation_rates
    ):

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

        plt.plot(
            time,
            release,
            linewidth=2,
            label=(
                f"k_deg = "
                f"{rate_per_hour:.3f} 1/hr"
            )
        )

        # ------------------------------------------------
        # t50
        # ------------------------------------------------

        t50_index = (
            abs(release - 50)
        ).argmin()

        t50 = time[t50_index]

        # ------------------------------------------------
        # t90
        # ------------------------------------------------

        t90_index = (
            abs(release - 90)
        ).argmin()

        t90 = time[t90_index]

        print()
        print(
            f"Degradation rate: "
            f"{rate_per_hour:.3f} 1/hour"
        )

        print(
            f"t50: {t50:.2f} hours"
        )

        print(
            f"t90: {t90:.2f} hours"
        )

    # ------------------------------------------------
    # Graph formatting
    # ------------------------------------------------

    plt.xlabel(
        "Time (hours)"
    )

    plt.ylabel(
        "Cumulative Drug Released (%)"
    )

    plt.title(
        "Effect of Polymer Degradation "
        "on Nanoparticle Drug Release"
    )

    plt.xlim(
        0,
        100
    )

    plt.ylim(
        0,
        100
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend(
        title="Degradation Rate"
    )

    plt.tight_layout()

    plt.savefig(
        "polymer_degradation_profiles.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()