import json
import random

# Function to generate a conversation
def generate_conversation(conv_id, language, inject_issues=False):
    # Language-specific templates for more natural variation
    agent_templates = {
        "english": [
            "Hello, this is from EMI collection. How can I help?",
            "Hi, thanks for calling EMI collection. How may I assist you today?",
            "Good day! I'm calling from EMI collection. What can I do for you?"
        ],
        "hinglish": [
            "Hello, ye EMI collection se bol raha hoon. Kaise madad kar sakta hoon?",
            "Hi, EMI collection se baat kar raha hoon. Aapko kya help chahiye?",
            "Namaste, EMI collection mein aapka swagat hai. Kaise madad karun?"
        ],
        "hindi": [
            "नमस्ते, यह EMI कलेक्शन से है। मैं कैसे मदद कर सकता हूँ?",
            "नमस्कार, EMI कलेक्शन से कॉल किया है। क्या मैं आपकी सहायता कर सकता हूँ?",
            "हैलो, EMI कलेक्शन में आपका स्वागत है। मैं आपकी किस प्रकार मदद करूँ?"
        ]
    }

    customer_templates = {
        "english": [
            "I need some time to pay.",
            "Can I get a few more days to make the payment?",
            "I'm having trouble paying on time."
        ],
        "hinglish": [
            "Sir, mujhe payment ke liye thoda time chahiye.",
            "Bhaiya, main thoda deri se payment karunga.",
            "Mujhe kal tak paise milenge, kya theek rahega?"
        ],
        "hindi": [
            "सर, कृपया EMI भुगतान जल्दी कर दीजिये।",
            "मुझे कुछ दिन और चाहिए, क्या आप मदद कर सकते हैं?",
            "मेरे पास अभी पैसे नहीं हैं, क्या आप समझ सकते हैं?"
        ]
    }

    followups = {
        "english": [
            ("Can you share your customer ID?", "Yes, it's 12345."),
            ("Would you like to schedule a callback?", "Yes, please call me back tomorrow."),
            ("Is there anything preventing you from making the payment today?", "Just waiting for my salary.")
        ],
        "hinglish": [
            ("Aapka customer ID kya hai?", "Mera ID 12345 hai."),
            ("Kya main aapko kal call karun?", "Haan, kal subah theek rahega."),
            ("Kya aapke paas koi aur prashn hai?", "Nahi, bas payment ka issue hai.")
        ],
        "hindi": [
            ("क्या आप अपना ग्राहक आईडी बता सकते हैं?", "हाँ, यह 12345 है।"),
            ("क्या मैं आपको कल कॉल कर सकता हूँ?", "हाँ, कल सुबह ठीक रहेगा।"),
            ("क्या आपको और कोई जानकारी चाहिए?", "नहीं, बस भुगतान का समय चाहिए।")
        ]
    }

    # Pick base turn texts
    agent_text = random.choice(agent_templates.get(language, agent_templates["english"]))
    customer_text = random.choice(customer_templates.get(language, customer_templates["english"]))

    turns = [
        {"role": "agent", "text": agent_text},
        {"role": "customer", "text": customer_text}
    ]

    # Optionally add 0-2 follow-up turn pairs for variety
    if random.random() < 0.6:
        num_followups = random.choice([0, 1, 2])
        for _ in range(num_followups):
            a, c = random.choice(followups.get(language, followups["english"]))
            turns.append({"role": "agent", "text": a})
            turns.append({"role": "customer", "text": c})

    metadata = {
        "call_duration_seconds": random.randint(60, 300),
        "outcome": random.choice(["payment_committed", "callback_scheduled", "escalated", "no_resolution"])
    }
    
    if inject_issues:
        # Inject quality issues
        issue_type = random.choice(["empty_turn", "duplicate_turn", "few_turns", "invalid_metadata", "language_mismatch", "garbled_text"])
        if issue_type == "empty_turn":
            turns.append({"role": "customer", "text": ""})
        elif issue_type == "duplicate_turn":
            turns.append(turns[-1])
        elif issue_type == "few_turns":
            turns = turns[:1]
        elif issue_type == "invalid_metadata":
            metadata["call_duration_seconds"] = -10
        elif issue_type == "language_mismatch":
            if language == "hindi":
                turns[0]["text"] = "Hello, this is from EMI collection."  # English instead
        elif issue_type == "garbled_text":
            turns[1]["text"] = "I n33d s0m3 t1m3 t0 p@y."  # Garbled
    
    return {
        "conversation_id": conv_id,
        "language": language,
        "turns": turns,
        "metadata": metadata
    }

# Generate 100 conversations
conversations = []
languages = ["hindi", "hinglish", "english"]
injected = []  # List of conv_ids with injected issues

for i in range(1, 101):
    conv_id = f"conv_{i:03d}"
    language = random.choice(languages)
    inject = random.random() < 0.35  # ~35% with issues
    if inject:
        injected.append(conv_id)
    conv = generate_conversation(conv_id, language, inject)
    conversations.append(conv)

# Write to JSONL
with open("raw_conversations.jsonl", "w", encoding="utf-8") as f:
    for conv in conversations:
        f.write(json.dumps(conv, ensure_ascii=False) + "\n")

print("Generated raw_conversations.jsonl")
print(f"Injected issues in conversations: {injected}")