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


def test_gaussian_smooth_rejects_invalid_kernel_parameters() -> None:
    """Reject a non-positive synthetic Gaussian standard deviation."""
    with pytest.raises(ValueError, match="parameters"):
        gaussian_smooth(np.zeros((2, 1)), standard_deviation_samples=0)
