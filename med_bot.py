import sys
import re
import ollama

try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except ImportError:
    HAS_TEXTBLOB = False

# Expanded regex patterns to catch root words and common brand/generic medications
MEDICATION_PATTERNS = [
    r"\bmedic\w*", r"\bdrug\w*", r"\bpill\w*", r"\btablet\w*", r"\bcapsul\w*",
    r"\bsyrup\w*", r"\bdosag\w*", r"\bprescrib\w*", r"\bpanadol\w*", r"\bparacetamol\w*",
    r"\bdisprin\w*", r"\bbrufen\w*", r"\bibuprofen\w*", r"\baspirin\w*", r"\btylenol\w*",
    r"\bantibiotic\w*", r"\bointment\w*", r"\bsteroid\w*"
]

# General non-medical topic triggers to block at Python layer before hitting LLM
NON_MEDICAL_PATTERNS = [
    r"\bcode\b", r"\bpython\b", r"\brecipe\b", r"\bcook\w*", r"\bsport\w*",
    r"\bcricket\b", r"\bmovie\w*", r"\bpolitics\b", r"\bmoney\b", r"\bfinance\b"
]

SYSTEM_PROMPT = """
You are a strict, domain-specific AI Health & Wellness Information Assistant.

STRICT DOMAIN SCOPE:
You are ONLY permitted to discuss topics strictly related to human health, general medical education, basic physiology, lifestyle wellness, exercise, and home recovery care.

STRICT DECLINATIONS:
1. NON-MEDICAL QUERIES: If a user asks about programming, cooking, history, entertainment, general knowledge, or any topic outside human health, respond ONLY with:
   "Sorry, I am a dedicated Medical Information Assistant and can only answer questions related to health and wellness."

2. MEDICATION BAN: You MUST NOT recommend, list, or suggest specific drug treatments, chemical medications, or pharmaceutical brand names.
   If asked for medication recommendations, respond ONLY with:
   "Sorry, I am a Medical Information Assistant and cannot recommend or mention specific medications or drugs. Please consult a doctor or pharmacist for medication guidance."

SAFETY & RESPONSE STRUCTURE:
- Always emphasize hydration, rest, nutrition, and consulting a certified healthcare professional.
- Always append this exact disclaimer at the end of every response:
  \n\n[Disclaimer: This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.]
"""

def contains_medication_query(text: str) -> bool:
    """Uses regex boundaries to check for drug/medication terms."""
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in MEDICATION_PATTERNS)

def contains_non_medical_query(text: str) -> bool:
    """Pre-screens obvious non-health topics at the Python level."""
    text_lower = text.lower()
    return any(re.search(pattern, text_lower) for pattern in NON_MEDICAL_PATTERNS)

def detect_sentiment(text: str) -> str:
    """Detects high anxiety levels using TextBlob."""
    if not HAS_TEXTBLOB:
        return ""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity < -0.3:
        return "\n\n*(Note: It sounds like you might be feeling anxious or stressed. Please take a deep breath and consider reaching out to a healthcare professional.)*"
    return ""

def run_medical_chatbot():
    print("=" * 65)
    print("        🏥 STRICT DOMAIN-SPECIFIC MEDICAL ASSISTANT")
    print("=" * 65)

    system_message = {"role": "system", "content": SYSTEM_PROMPT}
    conversation_history = []
    MAX_HISTORY = 6  # Kept smaller to prevent jailbreaks via long context

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("\nAssistant: Thank you for using the Health Assistant. Stay safe!")
                break

            if not user_input:
                continue

            # Layer 1 Guardrail: Python Medication Block
            if contains_medication_query(user_input):
                print(
                    "\nAssistant: Sorry, I am a Medical Information Assistant and cannot recommend "
                    "or mention specific medications or drugs. Please consult a doctor or pharmacist for medication guidance."
                    "\n\n[Disclaimer: This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.]"
                )
                print("-" * 65)
                continue

            # Layer 2 Guardrail: Python Non-Medical Block
            if contains_non_medical_query(user_input):
                print(
                    "\nAssistant: Sorry, I am a dedicated Medical Information Assistant and can only answer questions related to health and wellness."
                )
                print("-" * 65)
                continue

            # Sentiment check
            sentiment_note = detect_sentiment(user_input)

            # Update context history
            conversation_history.append({"role": "user", "content": user_input})
            trimmed_history = conversation_history[-MAX_HISTORY:]
            full_payload = [system_message] + trimmed_history

            # LLM Call
            response = ollama.chat(model="llama3", messages=full_payload)
            bot_reply = response["message"]["content"]

            # Store reply in history
            conversation_history.append({"role": "assistant", "content": bot_reply})

            print(f"\nAssistant: {bot_reply}{sentiment_note}")
            print("-" * 65)

        except (KeyboardInterrupt, EOFError):
            print("\n\nAssistant: Session terminated.")
            break
        except Exception as e:
            print(f"\n[Error]: Could not connect to Ollama instance: {e}")
            break

if __name__ == "__main__":
    run_medical_chatbot()
