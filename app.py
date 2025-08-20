import streamlit as st
import os
import re
import json
from dotenv import load_dotenv
import pandas as pd
import google.generativeai as genai

# Load secrets
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found. Please add it to .env or secrets.toml")
genai.configure(api_key=api_key)

# Set page configuration
st.title("🧠 MCQ Quiz App")

# Columns for difficulty and number of questions
col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox("Select the difficulty level:", ["Easy", "Medium", "Hard"])
with col2:
    num_questions = st.selectbox("Select the number of questions:", [3, 5, 10, 15])

# Session state initialization
for key in ["question_count", "max_questions", "results", "questions", "current_question", "quiz_started", "show_next"]:
    if key not in st.session_state:
        if key == "question_count":
            st.session_state[key] = 0
        elif key == "max_questions":
            st.session_state[key] = 0
        elif key in ["quiz_started", "show_next"]:
            st.session_state[key] = False
        else:
            st.session_state[key] = []
# Fetch questions from Gemini
def fetch_question(topic, difficulty, num_questions):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Generate {num_questions} multiple-choice questions on the topic: {topic}.
    Difficulty level: {difficulty}.
    Each question must have:
    - "question": the question text
    - "options": a list of 4 options
    - "answer": the correct option text
    - "explanation": a short explanation for the correct answer
    Return the result strictly as a JSON array.
    """
    response = model.generate_content(prompt)
    raw_data = response.text.strip()
    match = re.search(r'\[.*\]', raw_data, re.DOTALL)
    if not match:
        raise ValueError("No valid JSON found in the response.")
    return json.loads(match.group(0))

# Topic input
topic = st.text_input("Enter the topic of your quiz:")

# Generate quiz button
if st.button("Generate Quiz"):
    if not topic:
        st.error("Please enter a topic for the quiz.")
        st.stop()

    st.session_state["question_count"] = 0
    st.session_state["results"] = []
    st.session_state["max_questions"] = num_questions  # update max_questions
    try:
        st.session_state["questions"] = fetch_question(topic, difficulty, num_questions)
        st.session_state["current_question"] = st.session_state["questions"][0]
        st.session_state["quiz_started"] = True
    except Exception as e:
        st.error(f"Failed to generate quiz: {e}")
        st.stop()

# Quiz running
if st.session_state.get("quiz_started", False):
    q = st.session_state["current_question"]

    # Layout: Main column for question, side column for history
    col_question, col_history = st.columns([3, 1])

    with col_question:
        st.subheader(f"Q{st.session_state['question_count']+1}: {q['question']}")
        
        # Progress bar
        progress = (st.session_state['question_count']) / st.session_state['max_questions']
        st.progress(progress)
        
        # Form for answer submission
        with st.form(key=f"form_{st.session_state['question_count']}"):
            chosen = st.radio(
                "Choose your answer:",
                q["options"],
                index=0,
                disabled=st.session_state.get("answered_current", False)
            )

            # Submit button must be inside the form
            submit = st.form_submit_button("Submit Answer")

            if submit:
                is_correct = (chosen == q["answer"])
                st.session_state["results"].append({
                    "question": q["question"],
                    "chosen": chosen,
                    "correct": q["answer"],
                    "is_correct": is_correct,
                    "difficulty": difficulty,
                    "explanation": q["explanation"]
                })
                st.session_state["answered_current"] = True
                st.success("✅ Correct!" if is_correct else "❌ Wrong!")
                st.info(f"Explanation: {q['explanation']}")

# Next Question button (outside the form)
    if st.session_state.get("answered_current", False):
        if st.button("➡️ Next Question"):
            st.session_state["question_count"] += 1
            if st.session_state["question_count"] < st.session_state["max_questions"]:
                st.session_state["current_question"] = st.session_state["questions"][st.session_state["question_count"]]
                st.session_state["answered_current"] = False  # reset for next question
            else:
                st.session_state["quiz_started"] = False


    # Right column: past answers (scrollable)
    with col_history:
        st.markdown("### Your Answers")
        if st.session_state["results"]:
            answers_html = "<div style='height: 300px; overflow-y: auto; border: 1px solid #ddd; padding: 5px;'>"
            for idx, res in enumerate(st.session_state["results"], start=1):
                symbol = "✅" if res["is_correct"] else "❌"
                answers_html += f"<p><strong>Q{idx}:</strong> {res['chosen']} {symbol}</p>"
            answers_html += "</div>"
            st.markdown(answers_html, unsafe_allow_html=True)
        else:
            st.write("No answers yet")

# Results screen
if st.session_state["question_count"] >= st.session_state["max_questions"] and st.session_state["results"]:
    st.header("📊 Quiz Results & Analytics")

    df = pd.DataFrame(st.session_state["results"])
    score = df['is_correct'].sum()
    st.subheader(f"Final Score: {score}/{len(df)}")
    st.dataframe(df[["question", "chosen", "correct", "is_correct", "difficulty", "explanation"]])

    st.write("### Accuracy by Difficulty Level")
    acc = df.groupby('difficulty')['is_correct'].mean()
    st.bar_chart(acc)

    st.write("### Questions Breakdown")
    df["q_num"] = range(1, len(df) + 1)
    st.line_chart(df.set_index("q_num")["is_correct"].astype(int), use_container_width=True)

    st.download_button(
        label="Download Results as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='quiz_results.csv',
        mime='text/csv'
    )

    if st.button("🔄 Restart Quiz"):
        for key in ["question_count", "max_questions", "results", "questions", "current_question", "quiz_started", "show_next"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Quiz restarted! Please select options and topic again.")