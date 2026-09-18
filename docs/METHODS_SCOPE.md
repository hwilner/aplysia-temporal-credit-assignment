# Methods Scope

## Included methods

The retained utilities provide array-based transformations commonly useful when prototyping temporal credit-assignment workflows: conversion of padded one-based spike indices to logical matrices, Gaussian smoothing, exact-window downsampling, interval normalization, interval masks, component association scores, and within-interval peak-phase summaries. A deterministic non-negative matrix factorization helper remains available for caller-provided arrays.

## Scope limits

These utilities are generic computational building blocks. They do not include a bundled dataset, data loader, repository-local execution route, output writer, result summarizer, or figure generator. Their presence does not establish that any method is appropriate for a particular study or that any outcome follows from its use.

## Interpretation limits

Synthetic tests check defined program behavior, including shape handling, indexing conventions, and deterministic tie handling. They do not validate a scientific hypothesis, an experimental protocol, or an empirical conclusion.
