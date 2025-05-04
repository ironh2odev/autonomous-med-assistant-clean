# gnn/models/gnn_model.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import torch
import torch.nn as nn
import dgl
import dgl.nn as dglnn

class DrugGNN(nn.Module):
    def __init__(self, in_feats, hidden_feats, num_classes):
        super(DrugGNN, self).__init__()

        # First GraphSAGE layer
        self.conv1 = dglnn.SAGEConv(
            in_feats, hidden_feats, aggregator_type="mean"
        )

        # Second GraphSAGE layer
        self.conv2 = dglnn.SAGEConv(
            hidden_feats, num_classes, aggregator_type="mean"
        )

    def forward(self, graph, features):
        h = self.conv1(graph, features)
        h = torch.relu(h)
        h = self.conv2(graph, h)
        return h

# 🛠️ Helper: Quick model builder
def build_gnn_model(graph):
    in_feats = graph.ndata["feat"].shape[1]
    hidden_feats = 16  # I can tune this later
    num_classes = 2    # 0 = No dangerous interaction, 1 = Dangerous

    model = DrugGNN(in_feats, hidden_feats, num_classes)
    return model

if __name__ == "__main__":
    from data.drugs_graph import build_graph

    g = build_graph()
    model = build_gnn_model(g)
    print(model)

    dummy_input = g.ndata["feat"]
    out = model(g, dummy_input)
    print("Output shape:", out.shape)  # Should be (num_nodes, num_classes)
