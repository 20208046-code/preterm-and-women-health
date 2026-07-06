import os
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img

# === CONFIG ===
original_dir = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem/Ultrasound Fetus Dataset"
augmented_dir = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem/AugmentedDataset"
img_size = (224, 224)
augmentation_factor = 5
augment_classes = ['benign', 'normal']

# === Image Augmentation Generator ===
augmentor = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

print(f"🔍 Scanning folders in: {original_dir}")

# === Walk through subfolders ===
for root, dirs, files in os.walk(original_dir):
    class_name = os.path.basename(root)

    # Skip root if it's not a class folder
    if class_name not in augment_classes and class_name not in ['benign', 'normal', 'malignant']:
        continue

    print(f"📁 Processing folder: {class_name}")
    save_path = os.path.join(augmented_dir, class_name)
    os.makedirs(save_path, exist_ok=True)

    for img_name in files:
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"⏭️ Skipping non-image file: {img_name}")
            continue

        try:
            img_path = os.path.join(root, img_name)
            img = load_img(img_path, target_size=img_size)
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)

            # Save original
            array_to_img(x[0]).save(os.path.join(save_path, img_name))

            # Apply augmentation
            if class_name in augment_classes:
                aug_iter = augmentor.flow(x, batch_size=1)
                for i in range(augmentation_factor):
                    aug_img = next(aug_iter)[0]
                    save_name = f"{os.path.splitext(img_name)[0]}_aug{i+1}.jpg"
                    array_to_img(aug_img).save(os.path.join(save_path, save_name))

        except Exception as e:
            print(f"❌ Error processing {img_name}: {e}")

print("✅ Augmentation done.")
