from backend.llm_config import MAX_MESSAGES

memory = []

def load_memory():
    return memory

def save_message(role, content):
    memory.append({
        "role": role,
        "content": content
    })

    if len(memory) > MAX_MESSAGES:
        memory.pop(0)
