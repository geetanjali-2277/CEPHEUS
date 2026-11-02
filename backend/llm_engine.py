import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv
from backend.llm_config import MODEL_NAME, SYSTEM_PROMPT, MAX_MESSAGES

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

class LLMEngine:
    def __init__(self):
        self.model = MODEL_NAME
        # This list stores the conversation history for "Memory"
        self.memory = [] 

    def chat(self, user_input):
        # 1. Add User input to memory
        self.memory.append({"role": "user", "content": user_input})
        
        # 2. Keep memory from getting too long (Trim)
        if len(self.memory) > MAX_MESSAGES:
            self.memory = self.memory[-MAX_MESSAGES:]

        # 3. Build the payload with the System Prompt at the top
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.memory

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8, # Slightly higher for more "charismatic" personality
                max_tokens=1024
            )

            assistant_reply = response.choices[0].message.content.strip()
            
            # 4. Save Jarvis's reply to memory
            self.memory.append({"role": "assistant", "content": assistant_reply})
            
            return assistant_reply

        except Exception as e:
            print(f"[LLM ERROR] {e}")
            return "I'm having a bit of trouble with my communication array, Tony."

# ✅ GLOBAL INSTANCE
llm_instance = LLMEngine()

def ask_jarvis(prompt):
    return llm_instance.chat(prompt)