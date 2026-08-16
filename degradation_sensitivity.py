import matplotlib.pyplot as plt

from sensitivity import (
    run_simulation,
    calculate_t50_t90
)


def main():

    degradation_rates = [
        0.005,
        0.010,
        0.020,
        0.030,
        0.050
    ]

    t50_values = []
    t90_values = []

    for rate in degradation_rates:

        time, release = run_simulation(
            radius=200,
            temperature=37,
            pH=7.4,
            degradation_rate_per_hour=rate
        )

        t50, t90 = calculate_t50_t90(
            time,
            release
        )

        t50_values.append(t50)
        t90_values.append(t90)

        print(
            f"Degradation rate: {rate:.3f} 1/hour | "
            f"t50 = {t50:.2f} hr | "
            f"t90 = {t90:.2f} hr"
        )

    plt.figure(figsize=(10, 6))

    plt.plot(
        degradation_rates,
        t50_values,
        marker="o",
        label="t50"
    )

    plt.plot(
        degradation_rates,
        t90_values,
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

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "sensitivity_degradation.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()