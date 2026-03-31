import math

import pytest

from epi_learning.metrics import attack_rate, case_fatality_rate, odds_ratio, risk_ratio


def test_attack_rate_basic():
    assert math.isclose(attack_rate(50, 1000), 0.05)


def test_case_fatality_rate_basic():
    assert math.isclose(case_fatality_rate(3, 120), 0.025)


def test_risk_ratio_basic():
    rr = risk_ratio(exposed_cases=20, exposed_total=100, unexposed_cases=10, unexposed_total=100)
    assert math.isclose(rr, 2.0)


def test_attack_rate_invalid_population():
    with pytest.raises(ValueError):
        attack_rate(1, 0)


def test_odds_ratio_basic():
    # OR = (20*90) / (80*10) = 2.25
    assert math.isclose(odds_ratio(20, 80, 10, 90), 2.25)


def test_odds_ratio_zero_a():
    # a=0 is valid → OR = 0
    assert math.isclose(odds_ratio(0, 50, 10, 90), 0.0)


def test_odds_ratio_zero_b_raises():
    with pytest.raises(ZeroDivisionError):
        odds_ratio(10, 0, 5, 50)


def test_odds_ratio_zero_c_raises():
    with pytest.raises(ZeroDivisionError):
        odds_ratio(10, 50, 0, 50)


def test_odds_ratio_negative_raises():
    with pytest.raises(ValueError):
        odds_ratio(-1, 50, 10, 90)
