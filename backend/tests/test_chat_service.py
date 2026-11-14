
from app.chat_service import chat_with_candidate

question = "Who won yesterday's cricket match?"

answer = chat_with_candidate(question)

print("\nNageshAI:")
print(answer)
