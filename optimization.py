import numpy as np
import pandas as pd

from sensitivity import (
    run_simulation,
    calculate_t50_t90
)


def calculate_error(
    t50,
    t90,
    target_t50,
    target_t90
):
    """
    Calculate the squared error between
    predicted and target release times.
    """

    error_t50 = (
        t50 - target_t50
    ) ** 2

    error_t90 = (
        t90 - target_t90
    ) ** 2

    total_error = (
        error_t50
        + error_t90
    )

    return total_error


def optimize_nanoparticle():

    print("=" * 70)
    print("NANOPARTICLE DRUG-RELEASE OPTIMIZATION")
    print("=" * 70)

    # ------------------------------------------------
    # Target release profile
    # ------------------------------------------------

    target_t50 = 12.0
    target_t90 = 36.0

    print()
    print(
        f"Target t50: {target_t50:.2f} hours"
    )

    print(
        f"Target t90: {target_t90:.2f} hours"
    )

    # ------------------------------------------------
    # Search ranges
    # ------------------------------------------------

    radii = [
        50,
        100,
        150,
        200,
        250,
        300,
        350,
        400,
        450,
        500
    ]

    temperatures = [
        25,
        30,
        35,
        37,
        40
    ]

    pH_values = [
        5.5,
        6.0,
        6.5,
        7.0,
        7.4,
        8.0
    ]

    degradation_rates = [
        0.005,
        0.01,
        0.02,
        0.03,
        0.05
    ]

    # ------------------------------------------------
    # Search
    # ------------------------------------------------

    best_error = float("inf")

    best_design = None

    results = []

    total_combinations = (
        len(radii)
        * len(temperatures)
        * len(pH_values)
        * len(degradation_rates)
    )

    print()
    print(
        f"Testing {total_combinations:,} "
        "possible designs..."
    )

    count = 0

    for radius in radii:

        for temperature in temperatures:

            for pH in pH_values:

                for degradation in degradation_rates:

                    count += 1

                    time, release = run_simulation(
                        radius=radius,
                        temperature=temperature,
                        pH=pH,
                        degradation_rate_per_hour=(
                            degradation
                        )
                    )

                    t50, t90 = (
                        calculate_t50_t90(
                            time,
                            release
                        )
                    )

                    error = calculate_error(
                        t50,
                        t90,
                        target_t50,
                        target_t90
                    )

                    results.append({
                        "radius_nm": radius,
                        "temperature_C": temperature,
                        "pH": pH,
                        "degradation_rate_per_hour": (
                            degradation
                        ),
                        "t50_hours": t50,
                        "t90_hours": t90,
                        "error": error
                    })

                    if error < best_error:

                        best_error = error

                        best_design = {
                            "radius_nm": radius,
                            "temperature_C": temperature,
                            "pH": pH,
                            "degradation_rate_per_hour": (
                                degradation
                            ),
                            "t50_hours": t50,
                            "t90_hours": t90,
                            "error": error
                        }

    # ------------------------------------------------
    # Save all results
    # ------------------------------------------------

    dataframe = pd.DataFrame(
        results
    )

    dataframe = dataframe.sort_values(
        by="error"
    )

    dataframe.to_csv(
        "optimization_results.csv",
        index=False
    )

    # ------------------------------------------------
    # Print best design
    # ------------------------------------------------

    print()
    print("=" * 70)
    print("OPTIMIZED DESIGN")
    print("=" * 70)

    print(
        f"Radius: "
        f"{best_design['radius_nm']} nm"
    )

    print(
        f"Temperature: "
        f"{best_design['temperature_C']} °C"
    )

    print(
        f"pH: "
        f"{best_design['pH']}"
    )

    print(
        f"Degradation rate: "
        f"{best_design['degradation_rate_per_hour']}"
        " 1/hour"
    )

    print()
    print(
        f"Predicted t50: "
        f"{best_design['t50_hours']:.2f} hours"
    )

    print(
        f"Predicted t90: "
        f"{best_design['t90_hours']:.2f} hours"
    )

    print(
        f"Optimization error: "
        f"{best_design['error']:.4f}"
    )

    print()
    print(
        "Results saved to:"
    )

    print(
        "optimization_results.csv"
    )

    # ------------------------------------------------
    # Display top 10 designs
    # ------------------------------------------------

    print()
    print("=" * 70)
    print("TOP 10 DESIGNS")
    print("=" * 70)

    print(
        dataframe.head(10).to_string(
            index=False
        )
    )


if __name__ == "__main__":
    optimize_nanoparticle()