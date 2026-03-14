import json
import os

def clean_conversation(conv):
    """
    Clean a single conversation.
    Returns (cleaned_conv, rejection_reason) or (None, reason) if rejected.
    """
    turns = conv.get("turns", [])
    metadata = conv.get("metadata", {})
    
    # Check for fewer than 2 turns
    if len(turns) < 2:
        return None, "Fewer than 2 turns"
    
    # Remove empty or whitespace-only turns
    cleaned_turns = []
    for turn in turns:
        text = turn.get("text", "").strip()
        if text:
            cleaned_turns.append({"role": turn["role"], "text": text})
    
    if len(cleaned_turns) < 2:
        return None, "All turns empty after cleaning"
    
    # Remove duplicate consecutive turns
    deduped_turns = []
    prev = None
    for turn in cleaned_turns:
        if prev is None or not (turn["role"] == prev["role"] and turn["text"] == prev["text"]):
            deduped_turns.append(turn)
        prev = turn
    
    if len(deduped_turns) < 2:
        return None, "Fewer than 2 turns after deduplication"
    
    # Validate metadata
    duration = metadata.get("call_duration_seconds")
    if not isinstance(duration, int) or duration <= 0:
        return None, "Invalid call duration"
    
    outcome = metadata.get("outcome")
    if outcome not in ["payment_committed", "callback_scheduled", "escalated", "no_resolution"]:
        return None, "Invalid outcome"
    
    # Language mismatch check (simple heuristics)
    language = conv.get("language")
    texts = " ".join([t["text"] for t in deduped_turns])

    def looks_like_roman_hindi(s: str) -> bool:
        # Common romanized Hindi words/phrases (very small list)
        tokens = s.lower().split()
        hints = {"aap", "hai", "hai?", "kya", "kar", "ki", "jaldi", "dijiye", "kripya", "sir", "ji", "mujhe"}
        return any(t in hints for t in tokens)

    if language == "hindi":
        # Accept Devanagari or simple romanized Hindi
        has_devanagari = any(ord(c) > 127 for c in texts)
        if not has_devanagari and not looks_like_roman_hindi(texts):
            return None, "Language mismatch: labeled hindi but text appears English"
    
    # Garbled text: reject if there are many characters that are not letters/digits/whitespace/punctuation
    import unicodedata

    def is_allowed_char(c: str) -> bool:
        # Allow letters, numbers, whitespace, and punctuation (including Devanagari punctuation)
        cat = unicodedata.category(c)
        return cat[0] in {"L", "N", "Z", "P"}

    non_allowed_ratio = sum(1 for c in texts if not is_allowed_char(c)) / len(texts) if texts else 0
    if non_allowed_ratio > 0.3:
        return None, "Garbled or invalid text"
    
    cleaned_conv = {
        "conversation_id": conv["conversation_id"],
        "language": language,
        "turns": deduped_turns,
        "metadata": metadata
    }
    return cleaned_conv, None

def main():
    raw_file = "raw_conversations.jsonl"
    cleaned_file = "cleaned_conversations.jsonl"
    rejected_file = "rejected_conversations.jsonl"
    
    cleaned = []
    rejected = []
    
    with open(raw_file, "r", encoding="utf-8") as f:
        for line in f:
            conv = json.loads(line.strip())
            cleaned_conv, reason = clean_conversation(conv)
            if cleaned_conv:
                cleaned.append(cleaned_conv)
            else:
                conv["rejection_reason"] = reason
                rejected.append(conv)
    
    with open(cleaned_file, "w", encoding="utf-8") as f:
        for conv in cleaned:
            f.write(json.dumps(conv, ensure_ascii=False) + "\n")
    
    with open(rejected_file, "w", encoding="utf-8") as f:
        for conv in rejected:
            f.write(json.dumps(conv, ensure_ascii=False) + "\n")
    
    print(f"Cleaned: {len(cleaned)}, Rejected: {len(rejected)}")

if __name__ == "__main__":
    main()