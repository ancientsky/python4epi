"""Core epidemiological metrics used across lessons."""

from __future__ import annotations


def attack_rate(cases: int, population: int) -> float:
    """Compute attack rate as cases/population."""
    if population <= 0:
        raise ValueError("population must be > 0")
    if cases < 0:
        raise ValueError("cases must be >= 0")
    return cases / population


def case_fatality_rate(deaths: int, cases: int) -> float:
    """Compute case fatality rate as deaths/cases."""
    if cases <= 0:
        raise ValueError("cases must be > 0")
    if deaths < 0:
        raise ValueError("deaths must be >= 0")
    return deaths / cases


def risk_ratio(exposed_cases: int, exposed_total: int, unexposed_cases: int, unexposed_total: int) -> float:
    """Compute risk ratio from a 2x2 setup."""
    for value in (exposed_cases, exposed_total, unexposed_cases, unexposed_total):
        if value < 0:
            raise ValueError("counts must be non-negative")
    if exposed_total == 0 or unexposed_total == 0:
        raise ValueError("group totals must be > 0")

    risk_exposed = exposed_cases / exposed_total
    risk_unexposed = unexposed_cases / unexposed_total
    if risk_unexposed == 0:
        raise ZeroDivisionError("unexposed risk is zero")
    return risk_exposed / risk_unexposed


def odds_ratio(a: int, b: int, c: int, d: int) -> float:
    """Compute odds ratio from a 2×2 table.

    Parameters
    ----------
    a : int
        Exposed **and** diseased.
    b : int
        Exposed **and** not diseased.
    c : int
        Unexposed **and** diseased.
    d : int
        Unexposed **and** not diseased.

    Returns
    -------
    float
        Odds ratio ``(a * d) / (b * c)``.
    """
    for name, value in [("a", a), ("b", b), ("c", c), ("d", d)]:
        if value < 0:
            raise ValueError(f"{name} must be non-negative")
    if b * c == 0:
        raise ZeroDivisionError("b and c must both be > 0")
    return (a * d) / (b * c)
