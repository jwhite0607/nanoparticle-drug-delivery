import numpy as np
from scipy.integrate import solve_ivp


def diffusion_coefficient_temperature(
    temperature_celsius,
    D0,
    activation_energy
):
    """
    Calculate diffusion coefficient as a function
    of temperature using an Arrhenius relationship.
    """

    R = 8.314  # J/(mol*K)

    temperature_kelvin = (
        temperature_celsius + 273.15
    )

    D = D0 * np.exp(
        -activation_energy
        / (R * temperature_kelvin)
    )

    return D

def pH_diffusion_factor(
    pH,
    pKa=6.5,
    maximum_factor=5.0
):
    """
    Calculate an illustrative pH-dependent
    diffusion enhancement factor.

    This is a phenomenological model for a
    pH-responsive nanoparticle.

    Parameters
    ----------
    pH : float
        Environmental pH.

    pKa : float
        Illustrative ionization midpoint.

    maximum_factor : float
        Maximum diffusion enhancement.

    Returns
    -------
    float
        Dimensionless diffusion multiplier.
    """

    ionized_fraction = (
        1.0 /
        (
            1.0
            + 10 ** (pKa - pH)
        )
    )

    factor = (
        1.0
        + (maximum_factor - 1.0)
        * ionized_fraction
    )

    return factor
def effective_diffusion_coefficient(
    temperature_celsius,
    pH,
    D0,
    activation_energy,
    pKa=6.5,
    maximum_pH_factor=5.0
):
    """
    Calculate an effective diffusion coefficient
    incorporating both temperature and pH.

    D_effective =
        D_temperature * pH_factor
    """

    D_temperature = diffusion_coefficient_temperature(
        temperature_celsius,
        D0,
        activation_energy
    )

    pH_factor = pH_diffusion_factor(
        pH,
        pKa,
        maximum_pH_factor
    )

    D_effective = (
        D_temperature
        * pH_factor
    )

    return D_effective
def simulate_spherical_diffusion(
    radius_nm,
    diffusion_coefficient,
    total_time_hours=48,
    number_of_points=100
):
    """
    Simulate diffusion-controlled drug release
    from a spherical nanoparticle.
    """

    # Convert radius from nanometers to meters
    radius = radius_nm * 1e-9

    # Convert hours to seconds
    total_time = total_time_hours * 3600

    # Radial grid
    r = np.linspace(
        0,
        radius,
        number_of_points
    )

    dr = r[1] - r[0]

    # Initial concentration
    # Uniform concentration throughout particle
    initial_concentration = np.ones(
        number_of_points - 1
    )

    def diffusion_equation(
        time,
        concentration
    ):
        """
        Spherical Fickian diffusion equation.
        """

        C = np.zeros(
            number_of_points
        )

        C[:-1] = concentration

        # Perfect-sink boundary condition
        C[-1] = 0.0

        dCdt = np.zeros(
            number_of_points - 1
        )

        # Center of the sphere
        dCdt[0] = (
            6
            * diffusion_coefficient
            * (C[1] - C[0])
            / dr**2
        )

        # Interior points
        for i in range(
            1,
            number_of_points - 1
        ):

            dCdr = (
                C[i + 1] - C[i - 1]
            ) / (2 * dr)

            d2Cdr2 = (
                C[i + 1]
                - 2 * C[i]
                + C[i - 1]
            ) / dr**2

            spherical_term = (
                2 / r[i]
            ) * dCdr

            dCdt[i] = (
                diffusion_coefficient
                * (
                    d2Cdr2
                    + spherical_term
                )
            )

        return dCdt

    # Time points
    time_seconds = np.linspace(
        0,
        total_time,
        500
    )

    # Solve differential equation
    solution = solve_ivp(
        diffusion_equation,
        (0, total_time),
        initial_concentration,
        t_eval=time_seconds,
        method="BDF"
    )

    # Concentration at each radial position
    concentrations = solution.y

    # Calculate average concentration
    average_concentration = np.mean(
        concentrations,
        axis=0
    )

    # Fraction remaining
    fraction_remaining = (
        average_concentration
    )

    # Fraction released
    fraction_released = (
        1 - fraction_remaining
    )

    # Convert to percentage
    release_percent = (
        fraction_released * 100
    )

    # Keep results between 0 and 100%
    release_percent = np.clip(
        release_percent,
        0,
        100
    )

    # Convert seconds to hours
    time_hours = (
        solution.t / 3600
    )

    return (
        time_hours,
        release_percent
    )
def degradation_factor(
    time_seconds,
    degradation_rate,
    maximum_increase=4.0
):
    """
    Calculate how polymer degradation changes
    the diffusion coefficient over time.

    This is a phenomenological model.

    Parameters
    ----------
    time_seconds : float
        Time in seconds.

    degradation_rate : float
        Polymer degradation rate in 1/s.

    maximum_increase : float
        Maximum multiplier increase in diffusion.

    Returns
    -------
    float
        Dimensionless degradation multiplier.
    """

    factor = (
        1.0
        + maximum_increase
        * (
            1.0
            - np.exp(
                -degradation_rate
                * time_seconds
            )
        )
    )

    return factor
def simulate_degrading_nanoparticle(
    radius_nm,
    initial_diffusion_coefficient,
    degradation_rate,
    maximum_degradation_increase=4.0,
    total_time_hours=100,
    number_of_points=100
):
    """
    Simulate spherical drug diffusion while the
    nanoparticle polymer gradually degrades.
    """

    radius = radius_nm * 1e-9

    total_time = total_time_hours * 3600

    r = np.linspace(
        0,
        radius,
        number_of_points
    )

    dr = r[1] - r[0]

    initial_concentration = np.ones(
        number_of_points - 1
    )

    def diffusion_equation(
        time,
        concentration
    ):

        # Calculate degradation-dependent diffusion
        degradation_multiplier = degradation_factor(
            time,
            degradation_rate,
            maximum_degradation_increase
        )

        D = (
            initial_diffusion_coefficient
            * degradation_multiplier
        )

        C = np.zeros(
            number_of_points
        )

        C[:-1] = concentration

        # Perfect-sink boundary condition
        C[-1] = 0.0

        dCdt = np.zeros(
            number_of_points - 1
        )

        # Center of sphere
        dCdt[0] = (
            6
            * D
            * (C[1] - C[0])
            / dr**2
        )

        # Interior points
        for i in range(
            1,
            number_of_points - 1
        ):

            dCdr = (
                C[i + 1]
                - C[i - 1]
            ) / (2 * dr)

            d2Cdr2 = (
                C[i + 1]
                - 2 * C[i]
                + C[i - 1]
            ) / dr**2

            spherical_term = (
                2 / r[i]
            ) * dCdr

            dCdt[i] = D * (
                d2Cdr2
                + spherical_term
            )

        return dCdt

    time_seconds = np.linspace(
        0,
        total_time,
        500
    )

    solution = solve_ivp(
        diffusion_equation,
        (0, total_time),
        initial_concentration,
        t_eval=time_seconds,
        method="BDF"
    )

    concentrations = solution.y

    average_concentration = np.mean(
        concentrations,
        axis=0
    )

    fraction_remaining = (
        average_concentration
    )

    fraction_released = (
        1
        - fraction_remaining
    )

    release_percent = (
        fraction_released * 100
    )

    release_percent = np.clip(
        release_percent,
        0,
        100
    )

    time_hours = (
        solution.t / 3600
    )

    return (
        time_hours,
        release_percent
    )