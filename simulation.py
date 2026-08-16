import numpy as np

from model import release_percentage


def create_time_array(
    start=0.1,
    end=48,
    points=500
):
    """
    Create a time array in hours.
    """

    return np.linspace(
        start,
        end,
        points
    )


def simulate_release(
    radius_nm,
    k,
    n,
    time
):
    """
    Simulate drug release.

    radius_nm is currently included as a design
    parameter. In this Version 1 model, k and n
    control the release behavior.

    Later we will connect nanoparticle radius
    explicitly to a diffusion-based physical model.
    """

    release = release_percentage(
        time,
        k,
        n
    )

    return {
        "radius_nm": radius_nm,
        "time_hours": time,
        "release_percent": release
    }


def simulate_multiple_radii(
    radii,
    k_values,
    n,
    time
):
    """
    Run simulations for multiple nanoparticle radii.
    """

    results = []

    for radius, k in zip(
        radii,
        k_values
    ):

        result = simulate_release(
            radius_nm=radius,
            k=k,
            n=n,
            time=time
        )

        results.append(result)

    return results