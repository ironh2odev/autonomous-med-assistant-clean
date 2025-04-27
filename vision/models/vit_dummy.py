# vision/models/vit_dummy.py

import torch
from PIL import Image
from torchvision import transforms
from timm import create_model

# Load pretrained Vision Transformer model
model = create_model("vit_base_patch16_224", pretrained=True)
model.eval()

# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Diagnosis labels
CLASSES = ["Pneumonia", "No Finding", "Effusion", "Infiltration", "Edema"]

# Doctor-style interpretation notes
def generate_notes(label, confidence):
    if label == "Pneumonia":
        return "X-ray suggests pneumonia. Recommend antibiotics and follow-up imaging."
    elif label == "No Finding":
        return "No abnormalities observed. Imaging appears normal."
    elif label == "Effusion":
        return "Possible pleural effusion. Recommend thoracic ultrasound or CT for confirmation."
    elif label == "Infiltration":
        return "Infiltrates detected. Consider infectious or neoplastic causes."
    elif label == "Edema":
        return "Signs of pulmonary edema. Recommend correlation with cardiac function."
    else:
        return "Unclear findings. Further evaluation recommended."

def diagnose_image(image_path: str) -> dict:
    """
    Runs a diagnosis on the input X-ray image using a ViT model.

    Args:
        image_path (str): Path to the input image.

    Returns:
        dict: Diagnosis, confidence, and generated doctor's note.
    """
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        pred_idx = output.argmax(dim=1).item()
        confidence = torch.nn.functional.softmax(output, dim=1)[0, pred_idx].item()

    diagnosis = CLASSES[pred_idx % len(CLASSES)]
    note = generate_notes(diagnosis, confidence)

    return {
        "diagnosis": diagnosis,
        "confidence": round(confidence, 2),
        "note": note
    }
