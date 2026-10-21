"""Synthetic tests for array preprocessing utilities."""

from __future__ import annotations

import numpy as np
import pytest

from src.preprocessing import gaussian_smooth, spike_times_to_logical


def test_spike_times_to_logical_maps_one_based_indices() -> None:
    """Convert padded synthetic indices into the expected boolean matrix."""
    padded_times = np.array([[1, 2], [3, 0], [np.nan, 0]], dtype=float)

    logical = spike_times_to_logical(
        padded_times, acquisition_rate_hz=10, duration_seconds=1
    )

    assert logical.shape == (10, 2)
    assert logical[:, 0].nonzero()[0].tolist() == [0, 2]
    assert logical[:, 1].nonzero()[0].tolist() == [1]


def test_spike_times_to_logical_ignores_zero_and_nan_padding() -> None:
    """Ignore zero and non-finite padding in a synthetic spike-index matrix."""
    padded_times = np.array(
        [[2.0, 0.0], [0.0, 4.0], [np.nan, np.nan]], dtype=float
    )

    logical = spike_times_to_logical(
        padded_times, acquisition_rate_hz=10, duration_seconds=1
    )

    # Only the two valid one-based indices set true entries, at zero-based rows.
    assert logical.shape == (10, 2)
    assert logical[:, 0].nonzero()[0].tolist() == [1]
    assert logical[:, 1].nonzero()[0].tolist() == [3]
    assert int(logical.sum()) == 2


def test_spike_times_to_logical_rejects_out_of_range_indices() -> None:
    """Reject a synthetic index that exceeds the configured duration."""
    with pytest.raises(ValueError, match="outside"):
        spike_times_to_logical(
            np.array([[11.0]]), acquisition_rate_hz=10, duration_seconds=1
        )


def test_gaussian_smooth_preserves_shape_and_finite_values() -> None:
    """Smooth a synthetic activity matrix without changing its shape."""
    logical = np.array([[True], [False], [True], [False]], dtype=bool)

    smoothed = gaussian_smooth(
        logical, standard_deviation_samples=1, half_window_samples=2
    )

    assert smoothed.shape == logical.shape
    assert np.all(smoothed >= 0)
    assert np.all(np.isfinite(smoothed))


def test_gaussian_smooth_zero_half_window_returns_input_unchanged() -> None:
    """Return the synthetic matrix unchanged under a zero half-window.

    Pins the deterministic edge-case contract of ``gaussian_smooth`` when
    ``half_window_samples`` is zero: the finite kernel support collapses to
    the single lag-zero sample, normalization makes that one weight equal
    one, and centered trimming keeps the full convolution aligned, so the
    output reproduces the input values and shape exactly.
    """
    activity = np.array([[0.0, 1.0], [1.0, 0.0], [0.5, 0.25]], dtype=float)

    smoothed = gaussian_smooth(
        activity, standard_deviation_samples=1, half_window_samples=0
    )

    # With a zero half-window the normalized kernel is a single weight of 1.0
    # at lag zero, so smoothing is the identity map on the input matrix; the
    # assertions require the original shape, floating-point dtype, finite
    # values, and exact value equality rather than a smoothed redistribution.
    assert smoothed.shape == activity.shape
    assert np.issubdtype(smoothed.dtype, np.floating)
    assert np.all(np.isfinite(smoothed))
    assert np.array_equal(smoothed, activity)


def test_gaussian_smooth_rejects_invalid_kernel_parameters() -> None:
    """Reject a non-positive synthetic Gaussian standard deviation."""
    with pytest.raises(ValueError, match="parameters"):
        gaussian_smooth(np.zeros((2, 1)), standard_deviation_samples=0)
