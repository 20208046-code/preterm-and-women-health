"""Evaluate the pre-trained PyTorch ResNet (Resnet_fineTuning.pth) on Data/test."""
import os
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

PTH = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data/Resnet_fineTuning.pth"
TEST_DIR = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data/test"

model = torch.load(PTH, map_location="cpu", weights_only=False)
model.eval()
print("Final layer:", model.fc)

# Standard ImageNet preprocessing (most common for torchvision fine-tuning).
tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

ds = datasets.ImageFolder(TEST_DIR, transform=tf)
print("Test classes (index order):", ds.classes)
loader = DataLoader(ds, batch_size=32, shuffle=False)

correct = 0
total = 0
n_classes = len(ds.classes)
conf = [[0] * n_classes for _ in range(n_classes)]
with torch.no_grad():
    for x, y in loader:
        out = model(x)
        pred = out.argmax(1)
        for t, p in zip(y.tolist(), pred.tolist()):
            conf[t][p] += 1
        correct += (pred == y).sum().item()
        total += y.numel()

print(f"\nAccuracy on Data/test: {100*correct/total:.2f}%  ({correct}/{total})")
print("\nConfusion matrix (rows=true, cols=pred):", ds.classes)
for i, row in enumerate(conf):
    print(f"  {ds.classes[i]:10s} {row}")
