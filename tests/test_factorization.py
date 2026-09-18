"""Synthetic tests for temporal matrix-factorization helper utilities."""

from __future__ import annotations

import numpy as np
import pytest

from src.factorization import (
    downsample_mean,
    interval_mask,
    median_peak_phase,
    normalise_intervals,
    retraction_association_scores,
)


def test_downsample_mean_uses_exact_nonoverlapping_windows() -> None:
    """Average a synthetic time axis in exact adjacent windows."""
    matrix = np.array([[0.0], [2.0], [4.0], [6.0]])

    output = downsample_mean(matrix, factor=2)

    assert np.array_equal(output, np.array([[1.0], [5.0]]))


def test_downsample_mean_rejects_an_uneven_time_axis() -> None:
    """Reject synthetic inputs that cannot be evenly downsampled."""
    with pytest.raises(ValueError, match="not divisible"):
        downsample_mean(np.ones((3, 1)), factor=2)


def test_normalise_intervals_handles_single_and_multiple_input_forms() -> None:
    """Normalize equivalent synthetic interval layouts to the same bins."""
    assert np.array_equal(normalise_intervals(np.array([1, 20]), 10), np.array([[0, 1]]))
    assert np.array_equal(
        normalise_intervals(np.array([[1, 21], [20, 40]]), 10),
        np.array([[0, 1], [2, 3]]),
    )


def test_interval_mask_includes_both_interval_limits() -> None:
    """Mark the complete inclusive interval in a synthetic time axis."""
    mask = interval_mask(5, np.array([[1, 3]]))

    assert np.array_equal(mask, np.array([False, True, True, True, False]))


def test_retraction_association_scores_favors_interval_enrichment() -> None:
    """Score a component that is enriched in a supplied synthetic interval."""
    time_courses = np.array(
        [[0.0, 4.0], [0.0, 5.0], [3.0, 0.0], [4.0, 0.0]]
    )

    scores = retraction_association_scores(time_courses, np.array([[0, 1]]))

    assert int(np.argmax(scores)) == 1


def test_median_peak_phase_uses_earliest_tie() -> None:
    """Use the first maximum and median phase for synthetic intervals."""
    time_course = np.array([1.0, 3.0, 3.0, 0.0, 0.0, 5.0])

    phase = median_peak_phase(time_course, np.array([[0, 2], [3, 5]]))

    assert phase == 0.75
