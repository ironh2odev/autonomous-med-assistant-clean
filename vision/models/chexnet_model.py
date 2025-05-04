# vision/models/chexnet_model.py

import torch
import torch.nn as nn
from torchvision import models
from torchvision.models import DenseNet121_Weights
from PIL import Image
from torchvision import transforms

# === Model Setup ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load DenseNet121 with updated 'weights' argument
weights = DenseNet121_Weights.IMAGENET1K_V1
model = models.densenet121(weights=weights)

# Replace classifier for 14 chest X-ray labels
num_features = model.classifier.in_features
model.classifier = nn.Linear(num_features, 14)  # 14 diseases
model = model.to(device)
model.eval()

print(f"[INFO] CheXNet model loaded on device: {device}")

# Transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# List of labels from NIH ChestXray14
CLASSES = [
    "Atelectasis", "Cardiomegaly", "Effusion", "Infiltration", "Mass",
    "Nodule", "Pneumonia", "Pneumothorax", "Consolidation", "Edema",
    "Emphysema", "Fibrosis", "Pleural_Thickening", "Hernia"
]

def diagnose_image(image_path: str) -> dict:
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.sigmoid(output)[0]  # Multi-label probs

    # Pick top disease
    top_idx = probs.argmax().item()
    top_prob = probs[top_idx].item()

    return {
        "diagnosis": CLASSES[top_idx],
        "confidence": round(top_prob, 2)
    }