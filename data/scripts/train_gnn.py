import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from data.drugs_graph import build_graph
from gnn.models.gnn_model import DrugGNN

INPUT_DIM = int(os.getenv("INPUT_DIM", 10))
HIDDEN_DIM = int(os.getenv("HIDDEN_DIM", 16))
OUTPUT_DIM = int(os.getenv("OUTPUT_DIM", 2))
EPOCHS = int(os.getenv("EPOCHS", 30))
LR = float(os.getenv("LR", 0.01))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

graph = build_graph()

if graph.ndata.get("feat") is None or graph.ndata["feat"].shape[1] != INPUT_DIM:
    logger.warning(f"Replacing features with random {INPUT_DIM}-dim")
    graph.ndata["feat"] = torch.randn(graph.num_nodes(), INPUT_DIM)

graph = graph.to(device)

model = DrugGNN(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM).to(device)
logger.info(f"Model:\n{model}")

labels = torch.randint(0, OUTPUT_DIM, (graph.num_nodes(),), device=device)

loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)

for epoch in range(1, EPOCHS + 1):
    model.train()
    logits = model(graph, graph.ndata["feat"])
    loss = loss_fn(logits, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch == 1 or epoch % 5 == 0 or epoch == EPOCHS:
        acc = (logits.argmax(1) == labels).float().mean().item()
        logger.info(f"Epoch {epoch}/{EPOCHS} — Loss: {loss.item():.4f} — Acc: {acc:.4f}")

save_dir = os.path.join("gnn", "models")
os.makedirs(save_dir, exist_ok=True)
torch.save(model.state_dict(), os.path.join(save_dir, "gnn_model.pt"))
logger.info(f"Model saved at {save_dir}/gnn_model.pt")