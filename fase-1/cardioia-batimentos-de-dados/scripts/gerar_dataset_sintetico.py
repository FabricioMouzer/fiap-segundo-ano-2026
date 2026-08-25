"""Gera 150 registros cardiovasculares totalmente sintéticos.

Uso exclusivamente acadêmico. Não usar para diagnóstico, tratamento ou triagem.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 20260809
N = 150
OUT = Path("data/numericos/cardioia_pacientes_sinteticos.csv")
rng = np.random.default_rng(SEED)

def clip_round(value, low, high):
    return int(round(np.clip(value, low, high)))

rows = []
for i in range(1, N + 1):
    age = clip_round(rng.normal(55, 12), 29, 82)
    sex = rng.choice(["M", "F"], p=[0.52, 0.48])
    bmi = round(float(np.clip(rng.normal(27.4, 4.3), 18, 41)), 1)
    smoking = rng.choice(["never", "former", "current"], p=[0.51, 0.26, 0.23])
    diabetes_prob = np.clip(0.06 + (age - 35) * 0.004 + max(0, bmi - 28) * 0.015, 0.04, 0.38)
    diabetes = int(rng.random() < diabetes_prob)
    family = int(rng.random() < 0.31)
    sbp = clip_round(rng.normal(118 + (age - 40) * .45 + max(0, bmi - 25) * .7, 13), 90, 190)
    dbp = clip_round(rng.normal(76 + max(0, bmi - 25) * .35, 9), 55, 115)
    chol = clip_round(rng.normal(182 + age * .55 + (12 if smoking == "current" else 0), 35), 120, 360)
    glucose = clip_round(rng.normal(142 if diabetes else 92, 28 if diabetes else 13), 62, 230)
    resting_hr = clip_round(rng.normal(76 if smoking == "current" else 71, 10), 48, 112)
    max_hr = clip_round(rng.normal(205 - age * .72, 14), 82, 195)
    score = (-6.2 + age*.055 + (0.45 if sex == "M" else 0) + (sbp-115)*.018 +
             (chol-180)*.006 + ({"current":.8,"former":.25,"never":0}[smoking]) +
             diabetes*.75 + family*.55 + max(0,bmi-27)*.06)
    risk_prob = 1 / (1 + np.exp(-score))
    history = int(rng.random() < risk_prob)
    angina = int(rng.random() < np.clip(.06 + history*.38 + (age-40)*.003, .04, .62))
    pain = rng.choice(
        ["typical_angina","atypical_angina","non_anginal_pain","asymptomatic"]
        if history else ["non_anginal_pain","asymptomatic","asymptomatic","atypical_angina"]
    )
    rows.append({
        "patient_id_synthetic": f"SYN-{i:04d}", "age_years": age, "sex_at_birth": sex,
        "resting_sbp_mmHg": sbp, "resting_dbp_mmHg": dbp,
        "total_cholesterol_mg_dL": chol, "fasting_glucose_mg_dL": glucose,
        "resting_heart_rate_bpm": resting_hr, "max_heart_rate_bpm": max_hr,
        "bmi_kg_m2": bmi, "chest_pain_type": pain,
        "exercise_induced_angina": angina, "family_history_cad": family,
        "smoking_status": smoking, "diabetes_history": diabetes,
        "heart_disease_history": history,
        "cardio_risk_label_synthetic": "higher_simulated_risk" if risk_prob >= .5 else "lower_simulated_risk"
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"Arquivo criado: {OUT} | linhas: {len(rows)} | semente: {SEED}")
