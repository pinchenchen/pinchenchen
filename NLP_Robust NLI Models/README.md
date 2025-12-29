# Robust NLI Models: Mitigating Dataset Artifacts

## Overview
This project addresses the critical issue of **Dataset Artifacts** in Natural Language Inference (NLI). Standard models (like BERT) often learn ficial heuristics (e.g., associating the word "not" with *Contradiction*) rather than true semantic understanding. 

This repository implements a robust training pipeline that forces the model to learn from "hard" examples, utilizing **Targeted Fine-Tuning** and **Weighted Ensembling** to surpass standard baselines.

### Goal
To improve the generalization and robustness of an NLI model on the **SNLI (Stanford Natural Language Inference)** dataset, specifically focusing on hard-to-classify examples where standard BERT models fail.

## Methodology

### 1. Identifying Bias

This model intentionally captures the dataset biases (e.g., specific words correlating with specific labels)
- **Purpose:** To identify "easy" examples (where bias works) and "hard" examples (where bias fails).

### 2. Targeted Fine-Tuning on "Hard" Data
I segregated the dataset to isolate samples where the baseline model struggled.
- **Strategy:** I fine-tuned several BERT-base models specifically on these "hard" subsets to force the model to abandon superficial heuristics and learn deeper semantic relationships.

### 3. Weighted Ensemble Strategy
I implemented a **Weighted Voting Mechanism** that aggregates predictions from four distinct model checkpoints:
1.  **Baseline:** Standard BERT fine-tuned on full SNLI.
2.  **Debiased:** Model trained with bias-product limitations.
3.  **Hard-FT:** Model fine-tuned exclusively on hard examples.
4.  **Robust-Aug:** Model trained with additional robust data augmentation.

The final prediction is calculated as:
$$P_{final} = \text{argmax} \left( \sum_{i=1}^{k} w_i \times \log(P_{model\_i}) \right)$$

## Code Structure

- **`run.py`**: The main entry point for training and evaluation loops. Handles argument parsing for different model configurations.
- **`ensemble_simple.py`**: Implements the weighted ensemble logic. It loads probability distributions from multiple checkpoints and computes the optimal weighted average.
- **`filter_hard_data.py`**: A utility script used to preprocess the validation set, splitting it into "Easy" (heuristic-solvable) and "Hard" (requires reasoning) subsets for rigorous evaluation.

## Results

The rigorous ensemble approach demonstrated a clear improvement over the single-model baseline, particularly in overall accuracy.

| Model Strategy | Accuracy (Dev) |
| :--- | :--- |
| **Baseline (BERT-base)** | ~88.50% |
| **Weighted Ensemble (Final)** | **89.90%** |

## Tech Stack
- **Python**
- **PyTorch**
- **Hugging Face Transformers**
- **Scikit-learn**