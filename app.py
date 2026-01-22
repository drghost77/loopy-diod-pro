import streamlit as st

from brain.intent import detect_intent
from brain.frames import get_frame
from brain.analyzer import analyze
from brain.critical import critical_review
from brain.synthesis import synthesize

st.set_page_config(page_title="Cerveau Analytique MVP", layout="wide")

st.title("🧠 Cerveau Analytique — MVP")

question = st.text_area("Pose une question analytique ou stratégique :", height=120)

if st.button("Analyser") and question.strip():
    intent = detect_intent(question)
    frame = get_frame(intent)
    analysis = analyze(question, frame)
    critique = critical_review(question)
    response = synthesize(question, frame, analysis, critique)

    st.subheader("Résultat")
    st.text(response)