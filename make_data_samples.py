"""Generate small, recruiter-facing DATA SAMPLES (not the full datasets):
- a labeled ultrasound image grid (2 per class),
- a diverse sample CSV of the births data,
- a 'spreadsheet screenshot' PNG of the births data with real summary stats.
"""
import os
import shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
V1 = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1"
OUT = os.path.join(HERE, "docs", "data-samples")
US_OUT = os.path.join(OUT, "ultrasound")
os.makedirs(US_OUT, exist_ok=True)

# ---------- 1. Ultrasound sample images + labeled grid ----------
picks = {
    "benign": ["328_HC.png", "193_HC.png"],
    "malignant": ["504_HC.png", "475_HC.png"],
    "normal": ["236_HC.png", "328_HC.png"],
}
cell, pad, label_h = 300, 12, 40
cols, rows = 3, 2
grid = Image.new("RGB", (cols * cell + (cols + 1) * pad,
                          rows * cell + (rows + 1) * pad + label_h), "white")
draw = ImageDraw.Draw(grid)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
except Exception:
    font = ImageFont.load_default()

for c, (cls, files) in enumerate(picks.items()):
    # column label
    tx = pad + c * (cell + pad) + cell // 2
    draw.text((tx, 8), cls.upper(), fill="#1c598f", font=font, anchor="mt")
    for r, fn in enumerate(files):
        src = os.path.join(V1, "Data", "test", cls, fn)
        shutil.copy(src, os.path.join(US_OUT, f"{cls}_{fn}"))
        im = Image.open(src).convert("RGB").resize((cell, cell))
        x = pad + c * (cell + pad)
        y = label_h + pad + r * (cell + pad)
        grid.paste(im, (x, y))
grid.save(os.path.join(OUT, "ultrasound_samples.png"))
print("Saved ultrasound grid + 6 sample images")

# ---------- 2. Births data: diverse sample + stats + table screenshot ----------
# keep_default_na=False so the valid category "None" (zero previous births) is
# NOT misread as a missing value.
df = pd.read_csv(os.path.join(V1, "births.csv"), keep_default_na=False)
df["preterm_indicator"] = df["preterm_indicator"].astype(int)
total = len(df)
preterm_rate = 100 * df["preterm_indicator"].mean()
print(f"Total records: {total:,}  |  preterm rate: {preterm_rate:.2f}%")

colmap = {
    "age_group": "Age Group",
    "reported_race_ethnicity": "Race / Ethnicity",
    "previous_births": "Previous Births",
    "tobacco_use_during_pregnancy": "Tobacco Use",
    "adequate_prenatal_care": "Prenatal Care",
    "preterm_indicator": "Preterm",
}

# Build a DIVERSE preview from the distinct category combinations, mixing in
# some preterm=1 rows so both outcomes are visible.
uniq = df.drop_duplicates()
diverse = uniq.sample(n=10, random_state=7)
preterm_rows = uniq[uniq["preterm_indicator"] == 1].sample(n=4, random_state=7)
preview = pd.concat([diverse, preterm_rows]).drop_duplicates().head(12).reset_index(drop=True)

# Save a small, varied sample CSV
sample = uniq.sample(n=60, random_state=3).reset_index(drop=True)
sample.to_csv(os.path.join(OUT, "births_sample.csv"), index=False)
print(f"Saved births_sample.csv ({len(sample)} rows)")

# Render preview as a 'spreadsheet screenshot'
fig, ax = plt.subplots(figsize=(13, 5.0))
ax.axis("off")
ax.set_title(f"births.csv  —  {total:,} records  ·  preterm rate {preterm_rate:.1f}%  "
             f"(showing {len(preview)} sample rows)", fontsize=13, fontweight="bold",
             color="#1c598f", pad=22)
tbl = ax.table(cellText=preview.values, colLabels=[colmap[c] for c in preview.columns],
               cellLoc="center", loc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.9)
for (r, c), cell in tbl.get_celld().items():
    if r == 0:
        cell.set_facecolor("#1c598f"); cell.set_text_props(color="white", fontweight="bold")
    elif r % 2 == 0:
        cell.set_facecolor("#eef3f8")
plt.savefig(os.path.join(OUT, "births_preview.png"), dpi=130, bbox_inches="tight", pad_inches=0.35)
print("Saved births_preview.png")

# Print stats for the README
print("\n--- README STATS ---")
print("preterm_rate", round(preterm_rate, 2))
print(df["age_group"].value_counts().to_dict())
