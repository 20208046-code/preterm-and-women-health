"""
Second improvement attempt: PyTorch ResNet18 fine-tune with class-weighted loss.

Uses the clean Data/train / validation / test splits, standard ImageNet
preprocessing (unambiguous), heavy augmentation for the tiny benign/normal
classes, and saves the best model by validation BALANCED accuracy.
"""
import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

BASE = "/Users/hazem/Desktop/Pretem-and-Women-Health_Hazem 1/Data"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resnet18_ultrasound_v2.pth")
classes = ['benign', 'malignant', 'normal']
torch.manual_seed(0)
device = torch.device("cpu")

mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
train_tf = transforms.Compose([
    transforms.Resize((232, 232)),
    transforms.RandomCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])
eval_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])

train_ds = datasets.ImageFolder(os.path.join(BASE, "train"), transform=train_tf)
val_ds = datasets.ImageFolder(os.path.join(BASE, "validation"), transform=eval_tf)
test_ds = datasets.ImageFolder(os.path.join(BASE, "test"), transform=eval_tf)
assert train_ds.classes == classes, train_ds.classes
train_ld = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=0)
val_ld = DataLoader(val_ds, batch_size=64, num_workers=0)
test_ld = DataLoader(test_ds, batch_size=64, num_workers=0)

# Class-weighted loss (inverse frequency) to fight the imbalance.
counts = np.bincount([y for _, y in train_ds.samples], minlength=3)
weights = torch.tensor(counts.sum() / (3.0 * counts), dtype=torch.float32)
print("Train class counts:", counts.tolist(), "-> loss weights:", weights.tolist())
criterion = nn.CrossEntropyLoss(weight=weights.to(device))

model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model.fc = nn.Linear(model.fc.in_features, 3)
model = model.to(device)
opt = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)
sched = torch.optim.lr_scheduler.ReduceLROnPlateau(opt, factor=0.5, patience=2)


def evaluate(loader):
    model.eval()
    conf = np.zeros((3, 3), dtype=int)
    with torch.no_grad():
        for x, y in loader:
            p = model(x.to(device)).argmax(1).cpu().numpy()
            for t, pr in zip(y.numpy(), p):
                conf[t][pr] += 1
    recalls = [conf[i][i] / conf[i].sum() if conf[i].sum() else 0 for i in range(3)]
    acc = np.trace(conf) / conf.sum()
    return acc, float(np.mean(recalls)), recalls, conf


best_bal = -1.0
patience, bad = 6, 0
for epoch in range(1, 31):
    model.train()
    tot, run = 0, 0.0
    for x, y in train_ld:
        x, y = x.to(device), y.to(device)
        opt.zero_grad()
        loss = criterion(model(x), y)
        loss.backward()
        opt.step()
        run += loss.item() * x.size(0)
        tot += x.size(0)
    acc, bal, recalls, _ = evaluate(val_ld)
    sched.step(run / tot)
    flag = ""
    if bal > best_bal:
        best_bal = bal
        torch.save(model, OUT)
        bad = 0
        flag = "  <-- best, saved"
    else:
        bad += 1
    print(f"epoch {epoch:2d}  trainloss={run/tot:.3f}  val_acc={acc*100:.1f}%  "
          f"val_balanced={bal*100:.1f}%  recalls(ben/mal/nor)={[round(r*100) for r in recalls]}{flag}")
    if bad >= patience:
        print("early stop")
        break

print("\n=== BEST model on Data/test (clean) ===")
model = torch.load(OUT, weights_only=False)
acc, bal, recalls, conf = evaluate(test_ld)
print(f"TEST accuracy: {acc*100:.2f}%")
print(f"TEST BALANCED accuracy: {bal*100:.2f}%")
print("Per-class recall:", {classes[i]: f"{recalls[i]*100:.1f}%" for i in range(3)})
print("Confusion (rows=true, cols=pred):", classes)
for i in range(3):
    print(f"  {classes[i]:10s} {conf[i].tolist()}")
