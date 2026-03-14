# Part B Writeup

## Model Choice
I chose Qwen2.5-0.5B-Instruct because it's small (<1B params), fits on T4, and has good instruction-following capabilities. It's better than SmolLM for this task as Qwen handles multilingual better.

## LoRA Configuration
- Rank (r): 8 - Low rank to keep trainable params low (~1M params).
- Alpha: 16 - Scaling factor for LoRA updates.
- Target modules: q_proj, v_proj - Common attention layers for efficiency.
- Dropout: 0.1 - Light regularization.

This config balances efficiency and effectiveness for small models.

## What Went Well
- Pipeline ran end-to-end on Colab.
- Model loaded and trained quickly.
- Inference showed some adaptation to Hinglish.

## What Didn't
- Training data is small (50 examples), so overfitting possible.
- Evaluation is heuristic-based, not perfect.
- Model outputs not always polite or on-topic.

## Improvements with More Time/Compute
1. Larger dataset: Use all cleaned data, augment with synthetic conversations.
2. Better evaluation: Use BLEU/ROUGE or human evaluation.
3. Hyperparameter tuning: Experiment with learning rates, epochs.
4. Multi-task: Train on multiple objectives (politeness, topic adherence).