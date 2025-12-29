"""
Note:

This repository contains the model architectures and training methodology developed for a coursework project. 

The full training pipeline and dataset loaders are omitted to respect academic integrity.

"""

import torch
import torch.nn as nn

INPUT_MEAN = [0.2788, 0.2657, 0.2629]
INPUT_STD = [0.2064, 0.1944, 0.2252]

class MLPPlanner(nn.Module):
    def __init__(
        self,
        n_track: int = 10,
        n_waypoints: int = 3,
    ):
        super().__init__()
        self.n_track = n_track
        self.n_waypoints = n_waypoints

        layers = []
        input_size = 2 * 2 * n_track
        hidden_size = [64, 32, 32, 32]

        for n_out in hidden_size:
            layers.append(torch.nn.Linear(input_size, n_out))
            layers.append(torch.nn.BatchNorm1d(n_out))
            layers.append(torch.nn.ReLU())
            input_size = n_out

        layers.append(torch.nn.Linear(n_out, 2 * n_waypoints))
        self.network = torch.nn.Sequential(*layers)

    def forward(self, track_left, track_right, **kwargs):
        track_all = torch.cat((track_left, track_right), dim=1).flatten(start_dim=1, end_dim=2)
        waypoints = self.network(track_all)
        return waypoints.view(-1, self.n_waypoints, 2)

class TransformerLayer(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.self_att = torch.nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
        self.mlp = torch.nn.Sequential(
            torch.nn.Linear(embed_dim, 4 * embed_dim), 
            torch.nn.ReLU(), 
            torch.nn.Linear(4 * embed_dim, embed_dim)
        )
        self.in_norm = torch.nn.LayerNorm(embed_dim)
        self.mlp_norm = torch.nn.LayerNorm(embed_dim)

    def forward(self, x):
        x_norm = self.in_norm(x)
        x = x + self.self_att(x_norm, x_norm, x_norm)[0]
        x = x + self.mlp(self.mlp_norm(x))
        return x
       
class TransformerPlanner(nn.Module):
    def __init__(
        self,
        n_track: int = 10,
        n_waypoints: int = 3,
        d_model: int = 64,
    ):
        super().__init__()
        self.n_track = n_track
        self.n_waypoints = n_waypoints
        self.query_embed = nn.Embedding(n_waypoints, d_model)
        
        self.network = nn.Sequential(
            nn.Linear(2, d_model),
            *[TransformerLayer(d_model, num_heads=8) for _ in range(4)],
        )
        self.output_layer = nn.Linear(d_model, 2)

    def forward(self, track_left, track_right, **kwargs):
        track_all = torch.cat((track_left, track_right), dim=1)
        waypoints = self.network(track_all)
        # Using the last n_waypoints tokens and adding learnable query embeddings
        waypoints = waypoints[..., -self.n_waypoints:, :] + self.query_embed.weight
        return self.output_layer(waypoints)

class CNNPlanner(torch.nn.Module):
    def __init__(
        self,
        n_waypoints: int = 3,
    ):
        super().__init__()
        self.n_waypoints = n_waypoints
        self.register_buffer("input_mean", torch.as_tensor(INPUT_MEAN), persistent=False)
        self.register_buffer("input_std", torch.as_tensor(INPUT_STD), persistent=False)
        
        c1 = 128
        layers = [
            nn.Conv2d(3, c1, kernel_size=7, stride=4, padding=3),
            nn.BatchNorm2d(c1),
            nn.ReLU(),
        ]

        c2 = 64
        for _ in range(3):
            layers.append(nn.Conv2d(c1, c2, kernel_size=3, stride=2, padding=1))
            layers.append(nn.BatchNorm2d(c2))
            layers.append(nn.ReLU())
            c1 = c2

        out_layer = [
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(c2, n_waypoints * 2),
        ]

        self.network = nn.Sequential(*(layers + out_layer))

    def forward(self, image, **kwargs):
        x = (image - self.input_mean[None, :, None, None]) / self.input_std[None, :, None, None]
        x = self.network(x)
        return x.view(-1, self.n_waypoints, 2)