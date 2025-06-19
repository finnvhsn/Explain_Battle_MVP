def build_prompt(task, answer_1, answer_2):
    return f"""
Du bist ein strenger, aber fairer Lehrer. Zwei Lernende haben dieselbe Frage beantwortet.

Frage:
{task}

Antwort 1:
{answer_1}

Antwort 2:
{answer_2}

Welche Antwort ist fachlich richtiger, klarer formuliert und bietet mehr Mehrwert für Lernende?

Antworte im folgenden Format:
Gewinner: <Antwort 1 oder Antwort 2>
Begründung: <kurzer Erklärungstext>
"""
