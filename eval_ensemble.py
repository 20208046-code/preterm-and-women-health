"""Test whether averaging EfficientNet (Keras) + ResNet18 (Torch) probabilities
on the clean Data/test set beats either model alone. They fail on opposite
classes, so the ensemble may recover all three."""
import os
os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")
import numpy as np
from PIL import Image
import torch
from torchvision import transforms
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as kimage

TEST = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data/test"
classes = ['benign', 'malignant', 'normal']

eff = load_model("efficientnet_fetal_ultrasound_model_v2.h5")
res = torch.load("resnet18_ultrasound_v2.pth", weights_only=False); res.eval()
res_tf = transforms.Compose([
    transforms.Resize((224, 224)), transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])


def eff_probs(path):
    arr = np.expand_dims(kimage.img_to_array(kimage.load_img(path, target_size=(224, 224))), 0)
    return eff.predict(arr, verbose=0)[0]


def res_probs(path):
    x = res_tf(Image.open(path).convert("RGB")).unsqueeze(0)
    with torch.no_grad():
        return torch.softmax(res(x), 1)[0].numpy()


def run(name, fn):
    conf = np.zeros((3, 3), int)
    for ti, c in enumerate(classes):
        d = os.path.join(TEST, c)
        for f in os.listdir(d):
            if not f.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            p = int(np.argmax(fn(os.path.join(d, f))))
            conf[ti][p] += 1
    rec = [conf[i][i]/conf[i].sum() if conf[i].sum() else 0 for i in range(3)]
    print(f"\n{name}: acc={100*np.trace(conf)/conf.sum():.2f}%  balanced={100*np.mean(rec):.2f}%")
    print("  recalls:", {classes[i]: f"{rec[i]*100:.0f}%" for i in range(3)})
    for i in range(3):
        print(f"  {classes[i]:10s} {conf[i].tolist()}")


run("Ensemble (avg)", lambda p: eff_probs(p) + res_probs(p))
