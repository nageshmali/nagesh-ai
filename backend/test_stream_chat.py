
from app.chat_service import stream_chat_with_candidate

question = "Tell me about QuantumRecSys."

print("NageshAI: ", end="", flush=True)

for chunk in stream_chat_with_candidate(question):
    print(chunk, end="", flush=True)

print()
