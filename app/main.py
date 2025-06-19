import json
from app.models.judge_prompt import build_prompt
import subprocess

def load_task(task_id):
    with open("data/tasks.json", encoding="utf-8") as f:
        tasks = json.load(f)
    return next((t for t in tasks if t["id"] == task_id), None)

def ask_ollama(prompt):
    """Sendet den Prompt an ein Ollama-Modell über CLI"""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

if __name__ == "__main__":
    task = load_task(1)
    print(f"\n📝 Aufgabe: {task['question']}")

    answer_1 = input("\nAntwort 1: ")
    answer_2 = input("Antwort 2: ")

    prompt = build_prompt(task["question"], answer_1, answer_2)
    print("\n⏳ Bewertung läuft...")

    result = ask_ollama(prompt)
    print("\n🔍 Ergebnis:\n", result)
