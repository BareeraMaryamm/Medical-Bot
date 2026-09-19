# Medical-Bot
A secure, responsible AI chatbot built with Llama3 via Ollama that answers ONLY health &amp; wellness queries. Features 5-layer safety guardrails to block non-medical topics &amp; drug recommendations using Regex, strict system prompting, and TextBlob sentiment analysis for anxiety detection. 100% offline &amp; safe.

🏥 Domain-Specific Medical AssistantA secure and responsible Domain-Specific AI Chatbot built with Llama 3 via Ollama that is strictly restricted to answer ONLY Health & Wellness related queries.
This bot will REFUSE any non-medical question like coding, cooking, sports, movies, finance etc.

🎯 Key Features
1. Strict Domain-Specific Design
The assistant is locked to human health, physiology, lifestyle wellness, exercise and home recovery care only.

2. Multi-Layer Safety Guardrails
Layer 1: Medication Ban: Uses 17+ expanded regex patterns medic_, drug_, panadol, brufen, paracetamol, aspirin, antibiotic etc. to block any drug recommendation.
Layer 2: Non-Medical Block: Python-level regex filter blocks code, python, recipe, cricket, movie, politics etc. before calling the LLM.
Layer 3: System Prompt Enforcement: Strong system prompt forces LLM to add medical disclaimer in every response.
Layer 4: Anti-Jailbreak: MAX_HISTORY = 6 to prevent long-context jailbreak attacks.
Layer 5: Sentiment Analysis: Integrated TextBlob to detect negative polarity / anxiety and show empathy message.

⚙️ Tech Stack
Python 3
Ollama + Llama3 Model
Regular Expressions (re) for guardrails
TextBlob for Sentiment Detection
ANSI Colors for beautiful CLI UI

🚀 How to Run
1. Install dependencies
pip install ollama textblob

2. Pull Llama3 model
ollama pull llama3

3. Run the bot
python app.py

💬 Example Queries
✅ Allowed: What are the benefits of drinking water? How to improve sleep quality?
❌ Blocked: Write python code, Give me recipe, Suggest medicine for headache -> Bot will show a safe refusal message.

⚠️ Disclaimer
This information is for educational purposes only and is not a substitute for professional medical advice.
