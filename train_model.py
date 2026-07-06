import os
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")  # use tf-keras (Keras 2 API)
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
from tensorflow.keras.callbacks import ReduceLROnPlateau
import matplotlib
matplotlib.use('Agg')  # headless: write figures to file, never open a GUI window
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.utils.class_weight import compute_class_weight

# === UPDATED: Path to the augmented dataset ===
dataset_dir = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/AugmentedDataset"
# Explicit class list so stray/empty folders (e.g. 'Data-Extracted') are ignored.
# This order also defines the label indices the backend (app.py) must use.
class_names = ['benign', 'malignant', 'normal']
img_size = 224
batch_size = 32
num_epochs = 20

# Keras EfficientNet expects pixel values in [0, 255] and normalizes internally.
# Do NOT rescale to [0, 1] here or the pretrained features collapse and the model
# never learns (accuracy stays at chance). Inference in app.py must match (no /255).
data_gen = ImageDataGenerator(
    validation_split=0.2
)

# === Data Generators ===
train_generator = data_gen.flow_from_directory(
    dataset_dir,
    classes=class_names,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = data_gen.flow_from_directory(
    dataset_dir,
    classes=class_names,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# === Labels and Class Weights ===
num_classes = len(train_generator.class_indices)
class_labels = list(train_generator.class_indices.keys())
print("\nClass indices:", train_generator.class_indices)

unique, counts = np.unique(train_generator.classes, return_counts=True)
print("\nTraining set class distribution:")
for i, count in zip(unique, counts):
    print(f"{class_labels[i]}: {count} samples")

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_generator.classes),
    y=train_generator.classes
)
class_weights_dict = dict(enumerate(class_weights))
print("\nClass Weights:", class_weights_dict)

# === Model Definition ===
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(img_size, img_size, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)
model = Model(inputs=base_model.input, outputs=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)

# === Training Phase 1 ===
model.fit(
    train_generator,
    epochs=num_epochs,
    validation_data=val_generator,
    callbacks=[lr_scheduler],
    class_weight=class_weights_dict
)

# === Fine-tuning Phase 2 ===
for layer in base_model.layers[-30:]:
    layer.trainable = True

model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    train_generator,
    epochs=5,
    validation_data=val_generator,
    callbacks=[lr_scheduler],
    class_weight=class_weights_dict
)

# === Save the Model (next to this script, where app.py loads it) ===
MODEL_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'efficientnet_fetal_ultrasound_model.h5')
model.save(MODEL_OUT)
print(f"\nModel saved as '{MODEL_OUT}'")

# === Final Evaluation ===
val_loss, val_acc = model.evaluate(val_generator)
print(f"\nFinal Validation Accuracy: {val_acc * 100:.2f}%")

# === Confusion Matrix (saved to a file, no GUI window so this runs headless) ===
print("\nGenerating confusion matrix on validation set...")
val_preds = model.predict(val_generator)
y_pred = np.argmax(val_preds, axis=1)
y_true = val_generator.classes

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels)
disp.plot(cmap='Blues', xticks_rotation=45)
plt.title("Confusion Matrix - Validation Set")
plt.tight_layout()
plt.savefig('confusion_matrix.png')
print("Confusion matrix saved as 'confusion_matrix.png'")

