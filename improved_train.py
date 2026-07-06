"""
Improved ultrasound classifier training.

Fixes the data-leakage problem: trains ONLY on the clean Data/train split,
validates on Data/validation, and tests on the untouched Data/test. Uses full
fine-tuning of EfficientNetB0 (not just a frozen head), on-the-fly augmentation,
class weighting for the imbalanced classes, and saves the BEST model by
validation accuracy.
"""
import os
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import BatchNormalization
from sklearn.utils.class_weight import compute_class_weight

BASE = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data"
TRAIN_DIR = os.path.join(BASE, "train")
VAL_DIR = os.path.join(BASE, "validation")
TEST_DIR = os.path.join(BASE, "test")
class_names = ['benign', 'malignant', 'normal']
img_size = 224
batch_size = 32
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "efficientnet_fetal_ultrasound_model_v2.h5")

# EfficientNet expects [0,255]; augment the training data (helps tiny classes).
train_gen = ImageDataGenerator(
    rotation_range=20, width_shift_range=0.1, height_shift_range=0.1,
    zoom_range=0.15, horizontal_flip=True, brightness_range=[0.8, 1.2],
    fill_mode='nearest',
).flow_from_directory(TRAIN_DIR, classes=class_names, target_size=(img_size, img_size),
                      batch_size=batch_size, class_mode='categorical', shuffle=True)

val_gen = ImageDataGenerator().flow_from_directory(
    VAL_DIR, classes=class_names, target_size=(img_size, img_size),
    batch_size=batch_size, class_mode='categorical', shuffle=False)

# Class weights from the (imbalanced) training labels.
cw = compute_class_weight('balanced', classes=np.unique(train_gen.classes), y=train_gen.classes)
class_weights = dict(enumerate(cw))
print("Class indices:", train_gen.class_indices)
print("Class weights:", class_weights)

# --- Model ---
base = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
x = base.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
out = Dense(len(class_names), activation='softmax')(x)
model = Model(base.input, out)

ckpt = ModelCheckpoint(OUT, monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
early = EarlyStopping(monitor='val_accuracy', patience=6, restore_best_weights=True, mode='max')
rlr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)

# Phase 1: freeze base, train the head.
base.trainable = False
model.compile(optimizer=Adam(1e-3), loss='categorical_crossentropy', metrics=['accuracy'])
print("\n=== Phase 1: train head (frozen base) ===")
model.fit(train_gen, epochs=6, validation_data=val_gen,
          class_weight=class_weights, callbacks=[ckpt, rlr])

# Phase 2: full fine-tune, but keep BatchNorm layers frozen (recommended for EfficientNet).
base.trainable = True
for layer in base.layers:
    if isinstance(layer, BatchNormalization):
        layer.trainable = False
model.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
print("\n=== Phase 2: full fine-tune (BN frozen) ===")
model.fit(train_gen, epochs=30, validation_data=val_gen,
          class_weight=class_weights, callbacks=[ckpt, early, rlr])

print(f"\nBest model saved to {OUT}")

# --- Final clean test evaluation ---
print("\n=== Evaluating BEST model on Data/test (clean, never seen) ===")
from tensorflow.keras.models import load_model
best = load_model(OUT)
test_gen = ImageDataGenerator().flow_from_directory(
    TEST_DIR, classes=class_names, target_size=(img_size, img_size),
    batch_size=batch_size, class_mode='categorical', shuffle=False)
probs = best.predict(test_gen, verbose=0)
y_pred = np.argmax(probs, axis=1)
y_true = test_gen.classes
acc = (y_pred == y_true).mean()
print(f"\nTEST accuracy: {acc*100:.2f}%")
# balanced (per-class) accuracy
per_class = []
conf = np.zeros((3, 3), dtype=int)
for t, p in zip(y_true, y_pred):
    conf[t][p] += 1
for i in range(3):
    n = conf[i].sum()
    per_class.append(conf[i][i] / n if n else 0)
print(f"BALANCED accuracy: {np.mean(per_class)*100:.2f}%")
print("Per-class recall:", {class_names[i]: f"{per_class[i]*100:.1f}%" for i in range(3)})
print("Confusion (rows=true, cols=pred):", class_names)
for i in range(3):
    print(f"  {class_names[i]:10s} {conf[i].tolist()}")
