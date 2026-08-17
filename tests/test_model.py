import numpy as np

from model import (
    diffusion_coefficient_temperature,
    pH_diffusion_factor,
    effective_diffusion_coefficient,
    simulate_spherical_diffusion,
    degradation_factor,
    simulate_degrading_nanoparticle,
)

from model_v3 import simulate_calibrated_release


def test_release_output_is_valid():
    time, release = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert len(time) == len(release)
    assert len(time) > 0
    assert np.all(np.isfinite(time))
    assert np.all(np.isfinite(release))
    assert np.all(release >= 0)
    assert np.all(release <= 100)


def test_time_array_is_increasing():
    time, release = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert time[0] == 0
    assert np.all(np.diff(time) > 0)


def test_release_generally_increases():
    time, release = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert np.all(np.diff(release) >= -1e-10)


def test_radius_affects_release():
    _, release_small = simulate_calibrated_release(
        radius_nm=100,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    _, release_large = simulate_calibrated_release(
        radius_nm=400,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert release_small[-1] >= release_large[-1]


def test_temperature_affects_release():
    _, release_low = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=20,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    _, release_high = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=40,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert release_high[-1] >= release_low[-1]


def test_ph_affects_release():
    _, release_low = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=5.5,
        degradation_rate_per_hour=0.005
    )

    _, release_high = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert not np.allclose(release_low, release_high)


def test_degradation_affects_release():
    _, release_low = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.001
    )

    _, release_high = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.01
    )

    assert not np.allclose(release_low, release_high)


def test_optimized_configuration_runs():
    time, release = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert len(time) == len(release)
    assert 0 <= release[-1] <= 100


# ---------------------------------------------------------
# Direct tests for model.py
# ---------------------------------------------------------


def test_effective_diffusion_coefficient_is_positive():
    D = effective_diffusion_coefficient(
        temperature_celsius=30,
        pH=7.0,
        D0=3e-16,
        activation_energy=25000
    )

    assert np.isfinite(D)
    assert D > 0


def test_effective_diffusion_coefficient_responds_to_ph():
    D_low = effective_diffusion_coefficient(
        temperature_celsius=30,
        pH=5.5,
        D0=3e-16,
        activation_energy=25000
    )

    D_high = effective_diffusion_coefficient(
        temperature_celsius=30,
        pH=7.0,
        D0=3e-16,
        activation_energy=25000
    )

    assert D_high > D_low


def test_spherical_diffusion_output_is_valid():
    time, release = simulate_spherical_diffusion(
        radius_nm=200,
        diffusion_coefficient=1e-16,
        total_time_hours=2,
        number_of_points=30
    )

    assert len(time) == len(release)
    assert len(time) > 0
    assert np.all(np.isfinite(time))
    assert np.all(np.isfinite(release))
    assert time[0] == 0
    assert np.all(np.diff(time) > 0)
    assert np.all(release >= 0)
    assert np.all(release <= 100)


def test_spherical_diffusion_release_increases():
    time, release = simulate_spherical_diffusion(
        radius_nm=200,
        diffusion_coefficient=1e-14,
        total_time_hours=2,
        number_of_points=30
    )

    assert release[-1] >= release[0]


def test_degradation_factor_starts_at_one():
    factor = degradation_factor(
        time_seconds=0,
        degradation_rate=0.005 / 3600,
        maximum_increase=4.0
    )

    assert np.isclose(factor, 1.0)


def test_degradation_factor_increases_with_time():
    rate = 0.005 / 3600

    factor_early = degradation_factor(
        time_seconds=3600,
        degradation_rate=rate,
        maximum_increase=4.0
    )

    factor_late = degradation_factor(
        time_seconds=10 * 3600,
        degradation_rate=rate,
        maximum_increase=4.0
    )

    assert factor_late > factor_early


def test_degradation_factor_has_expected_upper_limit():
    factor = degradation_factor(
        time_seconds=1e9,
        degradation_rate=0.005 / 3600,
        maximum_increase=4.0
    )

    assert np.isclose(
        factor,
        5.0,
        atol=1e-6
    )


def test_degrading_nanoparticle_output_is_valid():
    time, release = simulate_degrading_nanoparticle(
        radius_nm=200,
        initial_diffusion_coefficient=1e-16,
        degradation_rate=0.005 / 3600,
        total_time_hours=2,
        number_of_points=30
    )

    assert len(time) == len(release)
    assert len(time) > 0
    assert np.all(np.isfinite(time))
    assert np.all(np.isfinite(release))
    assert time[0] == 0
    assert np.all(np.diff(time) > 0)
    assert np.all(release >= 0)
    assert np.all(release <= 100)


def test_degrading_nanoparticle_release_changes_with_degradation():
    _, release_no_degradation = simulate_degrading_nanoparticle(
        radius_nm=200,
        initial_diffusion_coefficient=1e-16,
        degradation_rate=0,
        total_time_hours=2,
        number_of_points=30
    )

    _, release_with_degradation = simulate_degrading_nanoparticle(
        radius_nm=200,
        initial_diffusion_coefficient=1e-16,
        degradation_rate=0.01 / 3600,
        total_time_hours=2,
        number_of_points=30
    )

    assert not np.allclose(
        release_no_degradation,
        release_with_degradation
    )


def test_calibrated_release_is_valid():
    time, release = simulate_calibrated_release(
        radius_nm=200,
        temperature_celsius=30,
        pH=7.0,
        degradation_rate_per_hour=0.005
    )

    assert len(time) == len(release)
    assert len(time) > 0
    assert release.min() >= 0
    assert release.max() <= 100