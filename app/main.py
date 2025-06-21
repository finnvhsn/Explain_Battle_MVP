import streamlit as st
import json
import random
import subprocess
from app.models.judge_prompt import build_prompt

# === Funktionen ===

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

def extract_winner(result_text):
    """Extrahiert 'Antwort 1' oder 'Antwort 2' aus dem KI-Ergebnis"""
    for line in result_text.splitlines():
        if line.lower().startswith("gewinner:"):
            if "1" in line:
                return 1
            elif "2" in line:
                return 2
    return None







# === UI ===

st.set_page_config(page_title="ExplainBattle", layout="centered")
st.title("🧠 ExplainBattle – Wer erklärt besser?")
st.write("Zwei Erklärungen zur selben Frage. Die KI wählt den Gewinner.")

# === SESSION INIT ===
if "task" not in st.session_state:
    st.session_state.task = random.choice(load_tasks())
if "score_1" not in st.session_state:
    st.session_state.score_1 = 0
if "score_2" not in st.session_state:
    st.session_state.score_2 = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

task = st.session_state.task

st.subheader(f"❓ Aufgabe: {task['question']}")

with st.form("battle_form"):
    answer_1 = st.text_area("Antwort 1", height=100)
    answer_2 = st.text_area("Antwort 2", height=100)
    submitted = st.form_submit_button("🆚 Vergleichen")

if submitted:
    with st.spinner("Bewertung durch KI läuft..."):
        prompt = build_prompt(task["question"], answer_1, answer_2)
        result = ask_ollama(prompt)
        winner = extract_winner(result)
        if winner == 1:
            st.session_state.score_1 += 1
        elif winner == 2:
            st.session_state.score_2 += 1
        st.session_state.last_result = result

# Ergebnisanzeige
if st.session_state.last_result:
    st.success("🎯 Ergebnis")
    st.code(st.session_state.last_result, language="markdown")

# Punktestand anzeigen
st.markdown("---")
st.subheader("🏆 Punktestand")
col1, col2 = st.columns(2)
col1.metric("Antwort 1", st.session_state.score_1)
col2.metric("Antwort 2", st.session_state.score_2)

# Buttons unten
colA, colB = st.columns(2)
with colA:
    if st.button("🔄 Neue Aufgabe starten"):
        st.session_state.task = random.choice(load_tasks())
        st.session_state.last_result = None
        st.experimental_rerun()
with colB:
    if st.button("🧹 Zurücksetzen"):
        st.session_state.score_1 = 0
        st.session_state.score_2 = 0
        st.session_state.last_result = None
        st.experimental_rerun()
