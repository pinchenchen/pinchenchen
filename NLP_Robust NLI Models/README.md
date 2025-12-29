# Robust NLI Models: Mitigating Dataset Artifacts 🧠

## Overview
This project addresses the critical issue of **Dataset Artifacts** in Natural Language Inference (NLI). Standard models (like BERT) often learn superficial heuristics (e.g., associating the word "not" with *Contradiction*) rather than true semantic understanding. 

This repository implements a robust training pipeline that forces the model to learn from "hard" examples, utilizing **Targeted Fine-Tuning** and **Weighted Ensembling** to surpass standard baselines.

### Goal
To improve the generalization and robustness of an NLI model on the **SNLI (Stanford Natural Language Inference)** dataset, specifically focusing on hard-to-classify examples where standard BERT models fail.

---

## Methodology

My approach moves beyond simple fine-tuning by implementing a multi-stage training and ensemble strategy.

### 1. Identifying Bias
The first step involves training a model that intentionally captures dataset biases (e.g., hypothesis-only baseline) to identify "easy" examples (where bias works) and "hard" examples (where bias fails).

The table below illustrates the error rates, highlighting the performance gap between standard baselines and debiasing approaches.

![Table 1 Error Rates](https://github.com/pinchenchen/pinchenchen/blob/main/NLP_Robust%20NLI%20Models/Table%201_ER%20Type.png)
*Table 1: Error rates (1-accuracy) on SNLI dev set comparing Baseline and Debiased models.*

### 2. Targeted Fine-Tuning on "Hard" Data
Based on the bias identification, I segregated the dataset to isolate samples where the baseline model struggled.
- **Strategy:** I fine-tuned several BERT-base models specifically on these "hard" subsets to force the model to abandon superficial heuristics and learn deeper semantic relationships.

As shown below, fine-tuning specifically on hard examples significantly reduces the error rate on the "Hard" subset compared to the original baseline.

![Table 2 FineTuning Results](https://github.com/pinchenchen/pinchenchen/blob/main/NLP_Robust%20NLI%20Models/Table%202_FineTuning%20Result.png)
*Table 2: Error rates on SNLI dev set showing the impact of fine-tuning on hard examples.*

### 3. Weighted Ensemble Strategy
I implemented a **Weighted Voting Mechanism** that aggregates predictions from four distinct model checkpoints:
1.  **Baseline:** Standard BERT fine-tuned on full SNLI.
2.  **Debiased:** Model trained with bias-product limitations.
3.  **Hard-FT:** Model fine-tuned exclusively on hard examples.
4.  **Robust-Aug:** Model trained with additional robust data augmentation.

The final prediction is calculated as:
$$P_{final} = \text{argmax} \left( \sum_{i=1}^{k} w_i \times \log(P_{model\_i}) \right)$$

---

## Code Structure

- **`run.py`**: The main entry point for training and evaluation loops. Handles argument parsing for different model configurations.
- **`ensemble_simple.py`**: Implements the weighted ensemble logic. It loads probability distributions from multiple checkpoints and computes the optimal weighted average.
- **`filter_hard_data.py`**: A utility script used to preprocess the validation set, splitting it into "Easy" (heuristic-solvable) and "Hard" (requires reasoning) subsets for rigorous evaluation.

---

## Results

The rigorous ensemble approach demonstrated a clear improvement over the single-model baseline. By combining models with different strengths (General vs. Hard-focused), the final weighted ensemble achieved the lowest overall error rate.

![Table 3 Ensemble Results](https://github.com/pinchenchen/pinchenchen/blob/main/NLP_Robust%20NLI%20Models/Table%203_Ensemble%20Result.png)
*Table 3: Final error rates on SNLI dev set for various ensemble methods.*

| Model Strategy | Accuracy (Dev) |
| :--- | :--- |
| **Baseline (BERT-base)** | ~88.50% |
| **Weighted Ensemble (Final)** | **89.90%** |

## Tech Stack
- **Python**
- **PyTorch**
- **Hugging Face Transformers**
- **Scikit-learn**