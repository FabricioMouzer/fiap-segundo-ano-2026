"""Gera 100 imagens PNG de ECG sintético para experimentação acadêmica."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt

SEED = 20260809
OUT = Path("outputs/ecg_images")
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(SEED)

def ecg(t, hr, variant):
    period = 60 / hr
    phase = np.mod(t, period) / period
    def pulse(mu, sigma, amp):
        distance = np.minimum(np.abs(phase-mu), 1-np.abs(phase-mu))
        return amp*np.exp(-.5*(distance/sigma)**2)
    signal = (pulse(.18,.025,.12) + pulse(.38,.012,-.14) + pulse(.405,.010,1.0) +
              pulse(.435,.014,-.28) + pulse(.68,.055,.30))
    if variant == "st_variation": signal += pulse(.52,.07,.10)
    return signal + .025*np.sin(2*np.pi*.25*t) + rng.normal(0,.012,len(t))

manifest = []
for i in range(1, 101):
    variant = ["sinus_like","sinus_like","sinus_like","tachycardia","bradycardia","st_variation"][i % 6]
    hr = int(rng.integers(101,131) if variant == "tachycardia" else
             rng.integers(45,59) if variant == "bradycardia" else rng.integers(60,100))
    t = np.linspace(0,10,2500)
    y = ecg(t,hr,variant)
    fig, ax = plt.subplots(figsize=(12,3),dpi=120)
    ax.set_facecolor("#fffafa"); ax.set_xlim(0,10); ax.set_ylim(-.55,1.35)
    ax.set_xticks(np.arange(0,10.01,.2),minor=True); ax.set_yticks(np.arange(-.5,1.31,.1),minor=True)
    ax.set_xticks(np.arange(0,10.1,1)); ax.set_yticks(np.arange(-.5,1.31,.5))
    ax.grid(which="minor",color="#f7c7cf",linewidth=.35)
    ax.grid(which="major",color="#e999a8",linewidth=.65)
    ax.plot(t,y,color="#152238",linewidth=1.05)
    ax.set_title(f"ECG sintético {i:03d} | padrão: {variant} | FC: {hr} bpm",fontsize=9)
    ax.set_xlabel("Tempo (s)"); ax.set_ylabel("Amplitude normalizada")
    fig.tight_layout()
    name=f"ecg_sintetico_{i:03d}.png"
    fig.savefig(OUT/name,bbox_inches="tight"); plt.close(fig)
    manifest.append({"file":name,"variant":variant,"simulated_hr_bpm":hr,"synthetic":True})

(OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
print(f"Imagens criadas: {len(manifest)} | pasta: {OUT} | semente: {SEED}")
