from model_v3 import simulate_calibrated_release
import numpy as np


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