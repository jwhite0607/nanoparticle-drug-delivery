import numpy as np

from model import (
    diffusion_coefficient_temperature,
    pH_diffusion_factor,
    simulate_degrading_nanoparticle
)


def simulate_calibrated_release(
    radius_nm,
    temperature_celsius,
    pH,
    degradation_rate_per_hour,
    diffusion_scale=1.0,
    total_time_hours=100
):

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

    # Apply calibration factor
    initial_D = (
        D_temperature
        * pH_factor
        * diffusion_scale
    )

    degradation_rate = (
        degradation_rate_per_hour / 3600
    )

    time, release = simulate_degrading_nanoparticle(
        radius_nm=radius_nm,
        initial_diffusion_coefficient=initial_D,
        degradation_rate=degradation_rate,
        maximum_degradation_increase=(
            maximum_degradation_increase
        ),
        total_time_hours=total_time_hours
    )

    return time, np.clip(release, 0, 100)