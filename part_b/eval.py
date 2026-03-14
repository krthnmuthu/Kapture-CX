"""Simple evaluation script for the finetuned EMI collection agent.

This script generates responses for a set of test prompts and then scores each response
on basic heuristics:
  - Does the response include Hinglish/Hindi keywords?
  - Does the response mention payment-related terms?
  - Is the response non-empty and under a reasonable length?

Run this after training (or on the base model) to get a quick pass/fail scorecard.
"""

from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

try:
    from peft import PeftModel
except ImportError:
    PeftModel = None

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
ADAPTER_DIR = "./results"  # Where the notebook saves LoRA weights

PROMPTS = [
    "I need some time to pay my EMI.",
    "Can you please tell me how much I owe?",
    "I am not able to pay today, can I get an extension?",
    "My salary is delayed, I will pay next week.",
    "Your agent was rude and I want to speak to a manager.",
    "What happens if I miss the payment?",
    "Can you help me set up an auto-debit?",
    "I want to check my payment schedule.",
    "EMI ka amount batayein.",
    "Aap se baat karna mushkil ho raha hai, please help."
]

HINGLISH_KEYWORDS = [
    "sir", "ji", "aap", "kya", "hai", "kaha", "jaldi", "dijiye", "kripya", "paise",
    "payment", "EMI", "installment", "due", "kal", "kal tak"  # some English too
]

PAYMENT_KEYWORDS = ["payment", "EMI", "installment", "due", "pay", "paise", "amount"]


def score_response(resp: str) -> dict:
    text = resp.lower()
    has_hinglish = any(k in text for k in HINGLISH_KEYWORDS)
    on_topic = any(k in text for k in PAYMENT_KEYWORDS)
    non_empty = len(text.strip()) > 0
    short_enough = len(text.split()) < 100

    return {
        "hinglish": has_hinglish,
        "on_topic": on_topic,
        "non_empty": non_empty,
        "short_enough": short_enough,
    }


def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    if PeftModel is not None:
        try:
            model = PeftModel.from_pretrained(model, ADAPTER_DIR)
            print(f"Loaded LoRA adapter from {ADAPTER_DIR}")
        except Exception:
            print(f"No LoRA adapter found at {ADAPTER_DIR}; using base model")

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    return tokenizer, model


def generate_responses(tokenizer, model, prompts: List[str]) -> List[str]:
    model.eval()
    out = []
    for prompt in prompts:
        input_text = f"Instruction: {prompt}\nResponse:"
        inputs = tokenizer(input_text, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=120, do_sample=True, top_p=0.9, temperature=0.8)
        resp = tokenizer.decode(outputs[0], skip_special_tokens=True)
        out.append(resp)
    return out


def main():
    tokenizer, model = load_model()
    responses = generate_responses(tokenizer, model, PROMPTS)

    print("\n=== Evaluation scorecard ===")
    total = len(responses)
    scores = {"hinglish": 0, "on_topic": 0, "non_empty": 0, "short_enough": 0}

    for i, (prompt, resp) in enumerate(zip(PROMPTS, responses), start=1):
        result = score_response(resp)
        for k, v in result.items():
            if v:
                scores[k] += 1

        print(f"\nPrompt {i}: {prompt}")
        print(f"Response: {resp}")
        print("Checks:", ", ".join([f"{k}={'✅' if v else '❌'}" for k, v in result.items()]))

    print("\nSummary:")
    for k, v in scores.items():
        print(f"  {k}: {v}/{total} ({v/total:.0%})")


if __name__ == "__main__":
    main()
