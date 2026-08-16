import numpy as np

from model import (
    diffusion_coefficient_temperature,
    pH_diffusion_factor,
    simulate_degrading_nanoparticle
)


def simulate_burst_release(
    radius_nm,
    temperature_celsius,
    pH,
    degradation_rate_per_hour,
    burst_fraction=0.20,
    total_time_hours=100
):
    """
    Version 2 nanoparticle drug-release model.

    Adds an initial burst-release fraction to the
    original diffusion/degradation model.
    """

    # Base diffusion parameters
    D0 = 3e-16
    activation_energy = 25000

    pKa = 6.5
    maximum_pH_factor = 5.0

    maximum_degradation_increase = 4.0

    # Temperature effect
    D_temperature = diffusion_coefficient_temperature(
        temperature_celsius=temperature_celsius,
        D0=D0,
        activation_energy=activation_energy
    )

    # pH effect
    pH_factor = pH_diffusion_factor(
        pH=pH,
        pKa=pKa,
        maximum_factor=maximum_pH_factor
    )

    initial_D = D_temperature * pH_factor

    # Convert degradation rate from 1/hour to 1/second
    degradation_rate = (
        degradation_rate_per_hour / 3600
    )

    # Original diffusion/degradation model
    time, diffusion_release = (
        simulate_degrading_nanoparticle(
            radius_nm=radius_nm,
            initial_diffusion_coefficient=initial_D,
            degradation_rate=degradation_rate,
            maximum_degradation_increase=(
                maximum_degradation_increase
            ),
            total_time_hours=total_time_hours
        )
    )

    # Keep burst fraction between 0 and 1
    burst_fraction = np.clip(
        burst_fraction,
        0.0,
        1.0
    )

    # Add the initial burst
    release = (
        burst_fraction * 100
        + (1 - burst_fraction)
        * diffusion_release
    )

    # Make sure release stays physically bounded
    release = np.clip(
        release,
        0,
        100
    )

    return time, release