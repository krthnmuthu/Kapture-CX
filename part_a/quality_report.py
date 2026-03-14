import json
from collections import Counter

def load_jsonl(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line.strip()))
    return data

def analyze_data(data):
    total = len(data)
    languages = Counter(conv["language"] for conv in data)
    outcomes = Counter(conv["metadata"]["outcome"] for conv in data)
    avg_turns = sum(len(conv["turns"]) for conv in data) / total if total > 0 else 0
    return total, languages, outcomes, avg_turns

def main():
    raw = load_jsonl("raw_conversations.jsonl")
    cleaned = load_jsonl("cleaned_conversations.jsonl")
    rejected = load_jsonl("rejected_conversations.jsonl")
    
    print("=== Quality Report ===")
    print(f"Total Raw: {len(raw)}")
    print(f"Total Cleaned: {len(cleaned)}")
    print(f"Total Rejected: {len(rejected)}")
    
    # Rejection reasons
    reasons = Counter(conv.get("rejection_reason", "Unknown") for conv in rejected)
    print("\nRejection Reasons:")
    for reason, count in reasons.items():
        pct = (count / len(rejected)) * 100 if rejected else 0
        print(f"  {reason}: {count} ({pct:.1f}%)")
    
    # Language distribution
    print("\nLanguage Distribution:")
    raw_total, raw_langs, raw_outs, raw_avg = analyze_data(raw)
    print("Raw:")
    for lang, count in raw_langs.items():
        print(f"  {lang}: {count}")
    print(f"  Avg turns: {raw_avg:.1f}")
    
    clean_total, clean_langs, clean_outs, clean_avg = analyze_data(cleaned)
    print("Cleaned:")
    for lang, count in clean_langs.items():
        print(f"  {lang}: {count}")
    print(f"  Avg turns: {clean_avg:.1f}")
    
    # Outcome distribution
    print("\nOutcome Distribution:")
    print("Raw:")
    for out, count in raw_outs.items():
        print(f"  {out}: {count}")
    print("Cleaned:")
    for out, count in clean_outs.items():
        print(f"  {out}: {count}")

if __name__ == "__main__":
    main()