import streamlit as st
import json
import random
import subprocess
from app.models.judge_prompt import build_prompt

def load_tasks():
    with open("data/tasks.json", encoding="utf-8") as f:
        return json.load(f)

def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

# ==== STREAMLIT UI START ====

st.set_page_config(page_title="ExplainBattle", layout="centered")

st.title("🧠 ExplainBattle – Wer erklärt besser?")
st.write("Zwei Erklärungen zur selben Frage. Die KI wählt den Gewinner.")

tasks = load_tasks()
task = random.choice(tasks)

st.subheader(f"❓ Aufgabe: {task['question']}")

with st.form("battle_form"):
    answer_1 = st.text_area("Antwort 1", height=100)
    answer_2 = st.text_area("Antwort 2", height=100)
    submitted = st.form_submit_button("🆚 Vergleichen")

if submitted:
    with st.spinner("Bewertung durch KI läuft..."):
        prompt = build_prompt(task["question"], answer_1, answer_2)
        result = ask_ollama(prompt)
    st.success("🎯 Ergebnis")
    st.code(result, language="markdown")
