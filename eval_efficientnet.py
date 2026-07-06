"""Evaluate the trained EfficientNet (.h5) on Data/test for a fair comparison."""
import os
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
import numpy as np
from collections import Counter
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL = "efficientnet_fetal_ultrasound_model.h5"
TEST = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data/test"
labels = ['benign', 'malignant', 'normal']  # index order from training

model = load_model(MODEL)

conf = [[0]*3 for _ in range(3)]
correct = total = 0
preds_all = Counter()
for ti, cls in enumerate(labels):
    d = os.path.join(TEST, cls)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if not fn.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        img = image.load_img(os.path.join(d, fn), target_size=(224, 224))
        arr = np.expand_dims(image.img_to_array(img), 0)  # raw [0,255]
        p = int(np.argmax(model.predict(arr, verbose=0)[0]))
        conf[ti][p] += 1
        preds_all[labels[p]] += 1
        correct += (p == ti)
        total += 1

print(f"\nEfficientNet accuracy on Data/test: {100*correct/total:.2f}%  ({correct}/{total})")
print("Prediction distribution:", dict(preds_all))
print("\nConfusion (rows=true, cols=pred):", labels)
for i, row in enumerate(conf):
    print(f"  {labels[i]:10s} {row}")
