# Kapture CX ML Intern Take-Home Assignment

## Setup Instructions

1. Clone or download this repository.
2. Ensure you have Python 3.8+ installed.
3. Install dependencies: `pip install -r requirements.txt`
4. For Part B, upload `finetune.ipynb` to Google Colab and run it (free tier T4 should suffice).

## Project Structure

- `part_a/`: Data cleaning and quality analysis
- `part_b/`: LLM finetuning
- `README.md`: This file
- `requirements.txt`: Python dependencies

## Running the Code

### Part A
1. Generate raw data: Run `python part_a/generate_data.py` (if you create it) or use the provided `raw_conversations.jsonl`.
2. Clean data: `python part_a/clean_data.py`
3. Generate report: `python part_a/quality_report.py`
4. Read `part_a/writeup.md` for reflections.

### Part B
1. Open `part_b/finetune.ipynb` in Colab.
2. Run all cells to finetune the model and evaluate.
3. (Optional) Run `python part_b/eval.py` locally after training to generate a simple scorecard.
4. Read `part_b/finetune_writeup.md` for details.

## Notes
- All code is designed to run on Google Colab free tier.
- Cite any external resources used in the writeups.

# Kapture CX ML Intern Take-Home Assignment

This project demonstrates a complete machine learning pipeline for conversational AI.
It includes generating noisy customer-support conversations, building a data cleaning
and validation pipeline, analyzing dataset quality, and fine-tuning a small language
model (Qwen2.5-0.5B) using LoRA to act as a polite EMI collection agent in Hinglish.