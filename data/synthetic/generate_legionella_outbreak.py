"""Generate a synthetic Legionella outbreak line list for a nursing home.

Scenario: 松柏護理之家 (Pine and Cypress Nursing Home) — an outbreak of Legionnaires'
disease linked to a contaminated hot-water system.  The facility houses ~280
residents across 3 floors, each with 2 wings (A / B).  The water heater
serving floors 2–3 wing B is the primary source, so residents in those
areas have higher exposure risk (via showers and a hydrotherapy pool).

The generated CSV is designed for teaching epidemiological analysis:
  - Descriptive epidemiology (person / place / time)
  - Epidemic curve construction
  - 2×2 table analysis and risk ratios
  - Stratified analysis / logistic regression with multiple risk factors
  - Survival / time-to-event exploration (onset → hospitalisation → death)
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
SEED = 42
random.seed(SEED)

# ---------------------------------------------------------------------------
# Facility layout
# ---------------------------------------------------------------------------
FLOORS = [1, 2, 3]
WINGS = ["A", "B"]
ROOMS_PER_WING = 25  # rooms 01–25
BEDS_PER_ROOM = 2    # bed 1 or 2

# Not all rooms are fully occupied — we target ~280 residents
TARGET_RESIDENTS = 280

# ---------------------------------------------------------------------------
# Outbreak timeline
# ---------------------------------------------------------------------------
OUTBREAK_START = date(2026, 1, 10)   # first possible exposure
OUTBREAK_PEAK = date(2026, 1, 20)    # peak of the epidemic curve
OUTBREAK_END = date(2026, 2, 5)      # last onset date
INVESTIGATION_DATE = date(2026, 2, 10)  # date of investigation / data freeze

# ---------------------------------------------------------------------------
# Baseline prevalence of comorbidities (nursing-home elderly)
# ---------------------------------------------------------------------------
PROB_CHF = 0.25
PROB_DM = 0.35
PROB_CANCER = 0.15
PROB_COPD = 0.20
PROB_IMMUNOSUPPRESSED = 0.10
SMOKING_DIST = {"never": 0.45, "former": 0.40, "current": 0.15}
FUNCTIONAL_DIST = {"independent": 0.25, "assisted": 0.50, "bedridden": 0.25}

# ---------------------------------------------------------------------------
# Exposure probabilities
# ---------------------------------------------------------------------------
# Shower use depends on functional status
SHOWER_PROB = {"independent": 0.90, "assisted": 0.60, "bedridden": 0.05}
# Hydrotherapy pool — only independent/assisted residents
HYDRO_PROB = {"independent": 0.30, "assisted": 0.10, "bedridden": 0.00}

# ---------------------------------------------------------------------------
# Attack-rate model (logistic-ish weights → probability of infection)
# ---------------------------------------------------------------------------
# Base attack probability ~ 0.08 for low-risk residents
BASE_ATTACK_PROB = 0.08

RISK_WEIGHTS: dict[str, float] = {
    "floor_2_wingB": 0.25,   # near contaminated water heater
    "floor_3_wingB": 0.20,
    "floor_2_wingA": 0.10,
    "floor_3_wingA": 0.08,
    "shower_use": 0.18,      # primary aerosol exposure
    "hydro_use": 0.12,       # secondary aerosol exposure
    "copd": 0.10,
    "smoking_current": 0.08,
    "smoking_former": 0.04,
    "immunosuppressed": 0.10,
    "age_80_plus": 0.06,
    "chf": 0.04,
    "dm": 0.03,
    "cancer": 0.05,
}

# ---------------------------------------------------------------------------
# Severity model
# ---------------------------------------------------------------------------
# Given infection, probability of each severity tier
# Adjusted by risk factors below
BASE_SEVERITY = {
    "asymptomatic": 0.12,
    "mild": 0.28,
    "moderate": 0.30,
    "severe": 0.30,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _weighted_choice(options: dict[str, float]) -> str:
    """Pick a key from *options* dict weighted by its value."""
    keys = list(options.keys())
    weights = list(options.values())
    return random.choices(keys, weights=weights, k=1)[0]


def _bernoulli(p: float) -> int:
    return 1 if random.random() < p else 0


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _random_date_around(center: date, spread_days: int) -> date:
    """Return a date drawn from a triangular distribution centred on *center*."""
    offset = int(random.triangular(-spread_days, spread_days, 0))
    return center + timedelta(days=offset)


def _generate_rooms() -> list[dict]:
    """Create room/bed slots for the whole facility."""
    slots = []
    for floor in FLOORS:
        for wing in WINGS:
            for room_num in range(1, ROOMS_PER_WING + 1):
                for bed in range(1, BEDS_PER_ROOM + 1):
                    room_label = f"{floor}{wing}-{room_num:02d}"
                    slots.append({
                        "floor": floor,
                        "wing": wing,
                        "room": room_label,
                        "bed": bed,
                    })
    return slots


# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate_outbreak(n_residents: int = TARGET_RESIDENTS) -> pd.DataFrame:
    """Generate the full outbreak line list."""
    # Assign residents to rooms (random subset of all bed slots)
    all_slots = _generate_rooms()
    random.shuffle(all_slots)
    slots = all_slots[:n_residents]

    records: list[dict] = []

    for i, slot in enumerate(slots, start=1):
        rec: dict = {"case_id": f"R{i:03d}"}

        # Demographics
        rec["age"] = random.randint(60, 98)
        rec["sex"] = random.choice(["M", "F"])

        # Facility placement
        rec["floor"] = slot["floor"]
        rec["wing"] = slot["wing"]
        rec["room"] = slot["room"]
        rec["bed"] = slot["bed"]

        # Admission to facility (random date in the past 0.5–8 years)
        days_in_facility = random.randint(180, 2920)
        rec["facility_admission_date"] = (
            INVESTIGATION_DATE - timedelta(days=days_in_facility)
        ).isoformat()

        # Comorbidities
        rec["comorbidity_chf"] = _bernoulli(PROB_CHF)
        rec["comorbidity_dm"] = _bernoulli(PROB_DM)
        rec["comorbidity_cancer"] = _bernoulli(PROB_CANCER)
        rec["comorbidity_copd"] = _bernoulli(PROB_COPD)
        rec["immunosuppressed"] = _bernoulli(PROB_IMMUNOSUPPRESSED)

        # Smoking
        rec["smoking_history"] = _weighted_choice(SMOKING_DIST)

        # Functional status
        rec["functional_status"] = _weighted_choice(FUNCTIONAL_DIST)

        # Exposures
        rec["shower_use"] = _bernoulli(SHOWER_PROB[rec["functional_status"]])
        rec["hydrotherapy_use"] = _bernoulli(HYDRO_PROB[rec["functional_status"]])

        # --- Infection probability ---
        p_inf = BASE_ATTACK_PROB
        floor_wing_key = f"floor_{rec['floor']}_wing{rec['wing']}"
        p_inf += RISK_WEIGHTS.get(floor_wing_key, 0.0)
        if rec["shower_use"]:
            p_inf += RISK_WEIGHTS["shower_use"]
        if rec["hydrotherapy_use"]:
            p_inf += RISK_WEIGHTS["hydro_use"]
        if rec["comorbidity_copd"]:
            p_inf += RISK_WEIGHTS["copd"]
        if rec["smoking_history"] == "current":
            p_inf += RISK_WEIGHTS["smoking_current"]
        elif rec["smoking_history"] == "former":
            p_inf += RISK_WEIGHTS["smoking_former"]
        if rec["immunosuppressed"]:
            p_inf += RISK_WEIGHTS["immunosuppressed"]
        if rec["age"] >= 80:
            p_inf += RISK_WEIGHTS["age_80_plus"]
        if rec["comorbidity_chf"]:
            p_inf += RISK_WEIGHTS["chf"]
        if rec["comorbidity_dm"]:
            p_inf += RISK_WEIGHTS["dm"]
        if rec["comorbidity_cancer"]:
            p_inf += RISK_WEIGHTS["cancer"]

        p_inf = _clamp(p_inf, 0.01, 0.95)
        infected = _bernoulli(p_inf)

        if not infected:
            # Not infected
            rec["symptom_onset_date"] = ""
            rec["fever"] = 0
            rec["cough"] = 0
            rec["dyspnea"] = 0
            rec["confusion"] = 0
            rec["diarrhea"] = 0
            rec["clinical_severity"] = "not_ill"
            rec["lab_confirmed"] = 0
            rec["case_classification"] = "not_a_case"
            rec["hospitalized"] = 0
            rec["hospitalization_date"] = ""
            rec["icu_admission"] = 0
            rec["outcome"] = "survived"
            rec["death_date"] = ""
            rec["notification_date"] = ""
        else:
            # --- Determine severity ---
            severity_mod = dict(BASE_SEVERITY)
            # Higher-risk patients → shift towards severe
            severity_shift = 0.0
            if rec["age"] >= 85:
                severity_shift += 0.12
            elif rec["age"] >= 80:
                severity_shift += 0.06
            if rec["comorbidity_copd"]:
                severity_shift += 0.08
            if rec["comorbidity_chf"]:
                severity_shift += 0.06
            if rec["immunosuppressed"]:
                severity_shift += 0.10
            if rec["comorbidity_cancer"]:
                severity_shift += 0.06

            # Shift probability mass from asymptomatic/mild to severe
            shift = min(severity_shift, severity_mod["asymptomatic"] + severity_mod["mild"] - 0.05)
            severity_mod["asymptomatic"] = max(0.02, severity_mod["asymptomatic"] - shift * 0.3)
            severity_mod["mild"] = max(0.03, severity_mod["mild"] - shift * 0.7)
            severity_mod["severe"] += shift

            severity = _weighted_choice(severity_mod)
            rec["clinical_severity"] = severity

            # Onset date — triangular distribution around outbreak peak
            if severity == "asymptomatic":
                # Asymptomatic cases: assign an "infection date" as onset
                rec["symptom_onset_date"] = _random_date_around(
                    OUTBREAK_PEAK, 10
                ).isoformat()
            else:
                onset = _random_date_around(OUTBREAK_PEAK, 10)
                # Clamp to outbreak window
                onset = max(OUTBREAK_START, min(OUTBREAK_END, onset))
                rec["symptom_onset_date"] = onset.isoformat()

            # Symptoms depend on severity
            if severity == "asymptomatic":
                rec["fever"] = 0
                rec["cough"] = 0
                rec["dyspnea"] = 0
                rec["confusion"] = 0
                rec["diarrhea"] = 0
            elif severity == "mild":
                rec["fever"] = _bernoulli(0.70)
                rec["cough"] = _bernoulli(0.50)
                rec["dyspnea"] = _bernoulli(0.15)
                rec["confusion"] = _bernoulli(0.05)
                rec["diarrhea"] = _bernoulli(0.25)
            elif severity == "moderate":
                rec["fever"] = _bernoulli(0.90)
                rec["cough"] = _bernoulli(0.70)
                rec["dyspnea"] = _bernoulli(0.50)
                rec["confusion"] = _bernoulli(0.15)
                rec["diarrhea"] = _bernoulli(0.35)
            else:  # severe
                rec["fever"] = _bernoulli(0.95)
                rec["cough"] = _bernoulli(0.85)
                rec["dyspnea"] = _bernoulli(0.80)
                rec["confusion"] = _bernoulli(0.40)
                rec["diarrhea"] = _bernoulli(0.40)

            # Lab confirmation
            if severity == "asymptomatic":
                rec["lab_confirmed"] = _bernoulli(0.30)  # found via screening
            elif severity == "mild":
                rec["lab_confirmed"] = _bernoulli(0.50)
            else:
                rec["lab_confirmed"] = _bernoulli(0.85)

            # Case classification
            if rec["lab_confirmed"]:
                rec["case_classification"] = "confirmed"
            elif severity != "asymptomatic":
                rec["case_classification"] = "probable"
            else:
                rec["case_classification"] = "not_a_case"

            # Hospitalisation
            if severity == "severe":
                rec["hospitalized"] = _bernoulli(0.90)
            elif severity == "moderate":
                rec["hospitalized"] = _bernoulli(0.45)
            elif severity == "mild":
                rec["hospitalized"] = _bernoulli(0.05)
            else:
                rec["hospitalized"] = 0

            if rec["hospitalized"] and rec["symptom_onset_date"]:
                onset_dt = date.fromisoformat(rec["symptom_onset_date"])
                hosp_delay = random.randint(1, 5)
                rec["hospitalization_date"] = (
                    onset_dt + timedelta(days=hosp_delay)
                ).isoformat()
            else:
                rec["hospitalization_date"] = ""

            # ICU
            if rec["hospitalized"] and severity == "severe":
                rec["icu_admission"] = _bernoulli(0.40)
            else:
                rec["icu_admission"] = 0

            # Outcome (death)
            death_prob = 0.0
            if severity == "severe":
                death_prob = 0.25
                if rec["age"] >= 85:
                    death_prob += 0.10
                if rec["comorbidity_chf"]:
                    death_prob += 0.05
                if rec["immunosuppressed"]:
                    death_prob += 0.08
            elif severity == "moderate":
                death_prob = 0.04
                if rec["age"] >= 85:
                    death_prob += 0.03
            # mild / asymptomatic → death_prob stays 0

            died = _bernoulli(_clamp(death_prob))
            rec["outcome"] = "dead" if died else "survived"

            if died and rec["symptom_onset_date"]:
                onset_dt = date.fromisoformat(rec["symptom_onset_date"])
                death_delay = random.randint(3, 14)
                rec["death_date"] = (
                    onset_dt + timedelta(days=death_delay)
                ).isoformat()
            else:
                rec["death_date"] = ""

            # Notification date (1–4 days after onset for symptomatic cases)
            if severity != "asymptomatic" and rec["symptom_onset_date"]:
                onset_dt = date.fromisoformat(rec["symptom_onset_date"])
                notify_delay = random.randint(1, 4)
                rec["notification_date"] = (
                    onset_dt + timedelta(days=notify_delay)
                ).isoformat()
            else:
                rec["notification_date"] = ""

        records.append(rec)

    df = pd.DataFrame(records)

    # Sort by case_id
    df = df.sort_values("case_id").reset_index(drop=True)

    return df


def main() -> None:
    df = generate_outbreak(TARGET_RESIDENTS)

    out_path = Path(__file__).parent / "legionella_outbreak.csv"
    df.to_csv(out_path, index=False)

    # Summary statistics
    n_total = len(df)
    n_infected = (df["clinical_severity"] != "not_ill").sum()
    n_confirmed = (df["case_classification"] == "confirmed").sum()
    n_probable = (df["case_classification"] == "probable").sum()
    n_hosp = df["hospitalized"].sum()
    n_icu = df["icu_admission"].sum()
    n_dead = (df["outcome"] == "dead").sum()

    print(f"Generated {n_total} resident records → {out_path}")
    print(f"  Infected (any severity): {n_infected}  ({n_infected/n_total:.1%})")
    print(f"  Confirmed cases:         {n_confirmed}")
    print(f"  Probable cases:           {n_probable}")
    print(f"  Hospitalised:            {n_hosp}")
    print(f"  ICU admissions:          {n_icu}")
    print(f"  Deaths:                  {n_dead}  (CFR among infected: {n_dead/n_infected:.1%})")

    # Show sample rows
    print("\n--- Sample cases ---")
    cols_preview = [
        "case_id", "age", "sex", "floor", "wing", "room",
        "comorbidity_copd", "shower_use", "clinical_severity",
        "case_classification", "hospitalized", "outcome",
    ]
    print(df[cols_preview].head(15).to_string(index=False))


if __name__ == "__main__":
    main()
