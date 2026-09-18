"""Array preprocessing utilities for temporal activity matrices."""

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def spike_times_to_logical(
    spike_times: np.ndarray,
    acquisition_rate_hz: int = 1000,
    duration_seconds: int = 120,
) -> np.ndarray:
    """Convert padded one-based spike indices into a boolean activity matrix.

    Args:
        spike_times: Two-dimensional padded spike-index array with one column per
            feature. Zeros and non-finite values are treated as padding.
        acquisition_rate_hz: Positive number of samples per second.
        duration_seconds: Positive duration represented by the output matrix.

    Returns:
        Boolean time-by-feature matrix with true values at supplied spike indices.

    Raises:
        ValueError: If the input is not two-dimensional, timing parameters are
            invalid, or a supplied spike index is non-integral or out of range.
    """
    if acquisition_rate_hz <= 0 or duration_seconds <= 0:
        raise ValueError("Acquisition rate and duration must be positive")
    expected_samples = acquisition_rate_hz * duration_seconds
    values = np.asarray(spike_times, dtype=float)
    if values.ndim != 2:
        raise ValueError(f"Expected a 2D spike-time matrix, found shape {values.shape}")
    output = np.zeros((expected_samples, values.shape[1]), dtype=bool)
    for feature_index in range(values.shape[1]):
        times = values[:, feature_index]
        times = times[np.isfinite(times) & (times != 0)]
        if times.size == 0:
            continue
        if not np.all(np.equal(times, np.floor(times))):
            raise ValueError("Spike times must be integer sample indices")
        indices = times.astype(int)
        if np.any(indices < 1) or np.any(indices > expected_samples):
            raise ValueError("Spike time is outside the configured acquisition range")
        # Convert one-based sample indices to Python's zero-based row positions.
        output[indices - 1, feature_index] = True
    return output


def gaussian_smooth(
    logical_spikes: np.ndarray,
    standard_deviation_samples: int = 1000,
    half_window_samples: int = 2500,
) -> np.ndarray:
    """Smooth each feature trace with a normalized finite Gaussian kernel.

    Args:
        logical_spikes: Two-dimensional time-by-feature activity matrix.
        standard_deviation_samples: Positive Gaussian standard deviation in samples.
        half_window_samples: Non-negative half-width of the kernel support.

    Returns:
        Floating-point matrix with the same shape as ``logical_spikes``.

    Raises:
        ValueError: If the matrix is not two-dimensional or kernel parameters are
            invalid.
    """
    matrix = np.asarray(logical_spikes, dtype=float)
    if matrix.ndim != 2:
        raise ValueError(f"Expected a 2D logical-spike matrix, found shape {matrix.shape}")
    if standard_deviation_samples <= 0 or half_window_samples < 0:
        raise ValueError("Gaussian parameters must be positive or zero as applicable")
    window = np.arange(-half_window_samples, half_window_samples + 1)
    kernel = norm.pdf(window, 0, standard_deviation_samples)
    kernel = kernel / kernel.sum()
    output = np.empty_like(matrix, dtype=float)
    for feature_index in range(matrix.shape[1]):
        convolved = np.convolve(matrix[:, feature_index], kernel, mode="full")
        # Center trimming restores the input time axis after full convolution.
        output[:, feature_index] = convolved[half_window_samples : -half_window_samples or None]
    return output
