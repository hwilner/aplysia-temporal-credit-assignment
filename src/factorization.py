"""Deterministic helpers for temporal matrix factorization workflows.

The functions in this module accept caller-provided arrays only. They neither read
repository data nor write outputs.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.decomposition import NMF

from .preprocessing import gaussian_smooth, spike_times_to_logical


@dataclass(frozen=True)
class FactorizationOutcome:
    """Timing and diagnostic values from one deterministic factorization.

    Attributes:
        selected_component: Zero-based index of the selected component.
        pre_peak_phase: Median peak phase for the first activity segment.
        post_peak_phase: Median peak phase for the second activity segment.
        pre_retraction_score: Interval-association score of the selected component.
        reconstruction_error: Frobenius reconstruction error reported by NMF.
    """

    selected_component: int
    pre_peak_phase: float
    post_peak_phase: float
    pre_retraction_score: float
    reconstruction_error: float


def downsample_mean(matrix: np.ndarray, factor: int = 10) -> np.ndarray:
    """Mean-downsample a time-by-feature matrix by an exact integer factor.

    Args:
        matrix: Two-dimensional time-by-feature numeric array.
        factor: Positive number of input rows per output row.

    Returns:
        Time-downsampled matrix with the same feature count.

    Raises:
        ValueError: If the input is not two-dimensional, ``factor`` is not positive,
            or the time axis cannot be divided evenly.
    """
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2:
        raise ValueError(f"Expected a 2D matrix, found shape {values.shape}")
    if factor <= 0 or values.shape[0] % factor:
        raise ValueError(
            f"Time axis of length {values.shape[0]} is not divisible by factor {factor}"
        )
    return values.reshape(values.shape[0] // factor, factor, values.shape[1]).mean(axis=1)


def normalise_intervals(boundaries: object, downsample_factor: int = 10) -> np.ndarray:
    """Convert one-based start/end samples into sorted inclusive bin intervals.

    Args:
        boundaries: One interval or an array of paired start/end sample indices.
        downsample_factor: Positive number of source samples per output bin.

    Returns:
        Integer N-by-2 array of inclusive zero-based ``[start, end]`` bin indices.

    Raises:
        ValueError: If the boundary shape is unsupported, values are invalid, or an
            interval ends before it starts.
    """
    if downsample_factor <= 0:
        raise ValueError("Downsample factor must be positive")
    values = np.asarray(boundaries, dtype=float)
    if values.size == 0:
        raise ValueError("At least one interval is required")
    values = np.squeeze(values)
    if values.ndim == 1:
        if values.shape[0] != 2:
            raise ValueError(f"Expected two values for a single interval, found {values.shape}")
        pairs = values.reshape(1, 2)
    elif values.ndim == 2:
        if values.shape[0] == 2:
            pairs = values.T
        elif values.shape[1] == 2:
            pairs = values
        else:
            raise ValueError(f"Cannot identify start/end axis in shape {values.shape}")
    else:
        raise ValueError(f"Expected one- or two-dimensional boundaries, found {values.shape}")
    if not np.all(np.isfinite(pairs)):
        raise ValueError("Interval boundaries must be finite")
    # Convert one-based samples to zero-based bins while keeping both limits inclusive.
    bins = np.floor((pairs.astype(int) - 1) / downsample_factor).astype(int)
    if np.any(bins[:, 1] < bins[:, 0]):
        raise ValueError("Found an interval whose end precedes its start")
    return bins[np.argsort(bins[:, 0])]


def interval_mask(length: int, intervals: np.ndarray) -> np.ndarray:
    """Return a boolean mask spanning inclusive intervals on a time axis.

    Args:
        length: Positive length of the time axis.
        intervals: N-by-2 array of inclusive start/end indices.

    Returns:
        Boolean vector with true values for bins covered by ``intervals``.

    Raises:
        ValueError: If ``length`` is not positive or no interval overlaps the axis.
    """
    if length <= 0:
        raise ValueError("Time-course length must be positive")
    mask = np.zeros(length, dtype=bool)
    for start, end in intervals:
        clipped_start = max(int(start), 0)
        clipped_end = min(int(end), length - 1)
        if clipped_start <= clipped_end:
            mask[clipped_start : clipped_end + 1] = True
    if not mask.any():
        raise ValueError("No interval overlaps the supplied time axis")
    return mask


def retraction_association_scores(time_courses: np.ndarray, intervals: np.ndarray) -> np.ndarray:
    """Score components by mean activity inside versus outside supplied intervals.

    Args:
        time_courses: Time-by-component numeric activation matrix.
        intervals: Inclusive intervals in the same time-bin coordinates.

    Returns:
        One inside-minus-outside mean-activity score per component.

    Raises:
        ValueError: If the activations are not two-dimensional or intervals cover all
            time bins.
    """
    values = np.asarray(time_courses, dtype=float)
    if values.ndim != 2:
        raise ValueError(f"Expected time-by-component matrix, found {values.shape}")
    mask = interval_mask(values.shape[0], intervals)
    if mask.all():
        raise ValueError("Intervals cover all time bins; no comparison bins remain")
    return values[mask].mean(axis=0) - values[~mask].mean(axis=0)


def median_peak_phase(time_course: np.ndarray, intervals: np.ndarray) -> float:
    """Return the median earliest-maximal peak phase across supplied intervals.

    Args:
        time_course: One-dimensional component activation sequence.
        intervals: Inclusive intervals in the time-course coordinates.

    Returns:
        Median normalized peak phase, with zero for one-bin intervals.

    Raises:
        ValueError: If no supplied interval overlaps the time course.
    """
    values = np.asarray(time_course, dtype=float).reshape(-1)
    phases: list[float] = []
    for start, end in intervals:
        clipped_start = max(int(start), 0)
        clipped_end = min(int(end), values.shape[0] - 1)
        if clipped_start > clipped_end:
            continue
        segment = values[clipped_start : clipped_end + 1]
        relative_peak = int(np.argmax(segment))
        denominator = max(segment.shape[0] - 1, 1)
        phases.append(relative_peak / denominator)
    if not phases:
        raise ValueError("No interval overlaps the supplied time course")
    return float(np.median(phases))


def smooth_and_downsample(
    spike_times: np.ndarray,
    downsample_factor: int = 10,
    smoothing_standard_deviation_samples: int = 1000,
    smoothing_half_window_samples: int = 2500,
) -> np.ndarray:
    """Convert, smooth, and mean-downsample a padded spike-index matrix.

    Args:
        spike_times: Padded one-based spike-index matrix.
        downsample_factor: Positive number of source samples per output bin.
        smoothing_standard_deviation_samples: Positive Gaussian standard deviation.
        smoothing_half_window_samples: Non-negative Gaussian support half-width.

    Returns:
        Smoothed, downsampled time-by-feature matrix.

    Raises:
        ValueError: If a delegated conversion, smoothing, or downsampling validation
            check fails.
    """
    logical = spike_times_to_logical(spike_times)
    smoothed = gaussian_smooth(
        logical,
        standard_deviation_samples=smoothing_standard_deviation_samples,
        half_window_samples=smoothing_half_window_samples,
    )
    return downsample_mean(smoothed, factor=downsample_factor)


def fit_primary_factorization(
    pre_spike_times: np.ndarray,
    post_spike_times: np.ndarray,
    pre_retraction_boundaries: object,
    post_retraction_boundaries: object,
    n_components: int = 2,
    downsample_factor: int = 10,
    smoothing_standard_deviation_samples: int = 1000,
    smoothing_half_window_samples: int = 2500,
    max_iter: int = 1000,
) -> FactorizationOutcome:
    """Fit a deterministic NMF model to two caller-provided activity segments.

    Args:
        pre_spike_times: First padded spike-index matrix.
        post_spike_times: Second padded spike-index matrix.
        pre_retraction_boundaries: Inclusive interval boundaries for the first segment.
        post_retraction_boundaries: Inclusive interval boundaries for the second segment.
        n_components: Positive number of NMF components.
        downsample_factor: Positive number of source samples per output bin.
        smoothing_standard_deviation_samples: Positive Gaussian standard deviation.
        smoothing_half_window_samples: Non-negative Gaussian support half-width.
        max_iter: Positive maximum number of NMF iterations.

    Returns:
        Selected-component timing summary and factorization diagnostics.

    Raises:
        ValueError: If segment feature counts differ or delegated validation fails.
    """
    if n_components <= 0 or max_iter <= 0:
        raise ValueError("Component count and maximum iterations must be positive")
    pre = smooth_and_downsample(
        pre_spike_times,
        downsample_factor,
        smoothing_standard_deviation_samples,
        smoothing_half_window_samples,
    )
    post = smooth_and_downsample(
        post_spike_times,
        downsample_factor,
        smoothing_standard_deviation_samples,
        smoothing_half_window_samples,
    )
    if pre.shape[1] != post.shape[1]:
        raise ValueError(f"Segment feature counts differ: {pre.shape[1]} and {post.shape[1]}")
    pre_intervals = normalise_intervals(pre_retraction_boundaries, downsample_factor)
    post_intervals = normalise_intervals(post_retraction_boundaries, downsample_factor)
    combined = np.vstack([pre, post])
    estimator = NMF(
        n_components=n_components,
        init="nndsvda",
        solver="cd",
        beta_loss="frobenius",
        max_iter=max_iter,
        tol=1e-4,
        shuffle=False,
    )
    activations = estimator.fit_transform(combined)
    pre_activations = activations[: pre.shape[0]]
    post_activations = activations[pre.shape[0] :]
    scores = retraction_association_scores(pre_activations, pre_intervals)
    selected = int(np.argmax(scores))
    return FactorizationOutcome(
        selected_component=selected,
        pre_peak_phase=median_peak_phase(pre_activations[:, selected], pre_intervals),
        post_peak_phase=median_peak_phase(post_activations[:, selected], post_intervals),
        pre_retraction_score=float(scores[selected]),
        reconstruction_error=float(estimator.reconstruction_err_),
    )
