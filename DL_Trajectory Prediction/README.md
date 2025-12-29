# Autonomous Driving Trajectory Prediction

## Overview
This project explores different Deep Learning architectures to predict vehicle waypoints for autonomous navigation in the **SuperTuxKart** simulation environment. 

### GOAL
The goal was to design a planner that takes either **lane boundary coordinates** or **raw camera images** as input and outputs precise control waypoints $(x, y)$ for the next 3 time steps.

###

## Model Architectures

I implemented and compared three distinct architectures to handle this regression problem:
- MLP
- Transformer
- CNN

### 1. MLP Planner (Baseline)
A simple Multi-Layer Perceptron that flattens the track boundary inputs.
- **Input:** Left and right lane boundaries (Fixed number of points).
- **Structure:** `Linear` -> `BatchNorm` -> `ReLU`
- **Role:** Served as a baseline to validate data processing and coordinate transformation logic.

### 2. Transformer Planner (Attention-based)
A more advanced approach utilizing the attention mechanism to process track sequences.
- **Learnable Query Embeddings**
    - Instead of a standard encoder-decoder, I used a set of learnable query embeddings to "attend" to the track features.
    - `waypoints = network(track) + query_embed`
    - This allows the model to dynamically weigh the importance of different track segments (e.g., sharp turns vs. straight roads) when predicting the future trajectory.

### 3. CNN Planner (Vision-based)
A purely vision-based model that predicts waypoints directly from raw pixels, removing the dependency on pre-processed lane data.
- **Backbone:** Custom Convolutional Neural Network (Conv2d).
- **Head:** `AdaptiveAvgPool2d` followed by a Flatten and Linear projection to regression outputs.
- **Challenge:** Handling the high variance in lighting and textures compared to coordinate-based inputs.

## Training Strategy & Loss Function

Achieving high precision (Longitudinal Error < 0.20) required a carefully tuned loss function. Standard MSE was insufficient due to the imbalance between longitudinal (speed) and lateral (steering) deviation.

### Custom Loss Implementation
Designed a weighted **SmoothL1Loss** to balance the gradients:

```python
loss_fn_x = torch.nn.SmoothL1Loss(beta=0.0001) # Tighter constraint for X
loss_fn_y = torch.nn.SmoothL1Loss(beta=0.01)   # Looser constraint for Y

# Alpha blending to balance longitudinal vs lateral importance
loss = alpha * x_loss + (1 - alpha) * y_loss
```

- Beta Tuning: Used a much smaller beta for the X-axis (0.0001) to force the model to be extremely precise regarding the longitudinal distance (speed control).

- Optimization: Trained using AdamW with weight decay to prevent overfitting on the small dataset.

## Results
The models were evaluated based on Euclidean distance errors. The Transformer-based planner achieved the best trade-off between accuracy and inference speed.

| Model | Longitudinal Error | Lateral Error | Status |
| --- | --- | --- | --- |
| **MLP** | < 0.20 | < 0.55 | Pass |
| **Transformer** | **< 0.18** | **< 0.50** | Best |
| **CNN** | < 0.30 | < 0.45 | Pass |
