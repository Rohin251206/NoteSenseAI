import os
import streamlit as st
import PyPDF2
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("NoteSenseAI - Turn Notes to Quizzes in no time!!")

uploaded_file = st.file_uploader("Upload your notes (PDF)", type=["pdf"])
text=""
if uploaded_file:
    # Extract text from PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text()

questions_input = st.text_area("Enter how many questions you want per set - ")
if questions_input.strip():
    number_of_questions = int(questions_input.strip())
else:
    number_of_questions = 10
    # Summarize
if st.button("Generate Summary"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    summary = model.generate_content(f"Summarize this text in a short but detailed manner, and give it in bullet points:\n{text}")
    st.subheader("📝 Summary")
    st.write(summary.text)

# Quiz
if st.button("Generate Quiz"):
    model = genai.GenerativeModel("gemini-1.5-flash")
    quiz = model.generate_content(f"Create {number_of_questions} multiple-choice questions from this text:\n{text}")
    st.subheader("🎯 Quiz")
    st.write(quiz.text)
