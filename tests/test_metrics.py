import math

import pytest

from epi_learning.metrics import attack_rate, case_fatality_rate, risk_ratio


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
