import random
import streamlit as st
import emoji

# Initialize session state
if 'number' not in st.session_state:
    st.session_state.number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'remaining_attempts' not in st.session_state:
    st.session_state.remaining_attempts = 10  # Set max attempts
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = '🟡 Medium'
if 'range' not in st.session_state:
    st.session_state.range = "(1-100)"
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'guess' not in st.session_state:
    st.session_state.guess = 1

def set_difficulty(level):
    if level == "🟢 Easy":
        st.session_state.number = random.randint(1, 50)
        st.session_state.range = "(1-50)"
    elif level == "🟡 Medium":
        st.session_state.number = random.randint(1, 100)
        st.session_state.range = "(1-100)"
    elif level == "🔴 Hard":
        st.session_state.number = random.randint(1, 200)
        st.session_state.range = "(1-200)"
    st.session_state.difficulty = level
    st.session_state.attempts = 0
    st.session_state.remaining_attempts = 10  # Reset attempts
    st.session_state.message = ""
    st.session_state.game_over = False
    st.session_state.guess = None  # Ensure input resets properly
    st.rerun()

# UI Styling
st.markdown(
    """
    <style>
    .main {
        background-color: purple;
        text-align: center;
    }
    .stApp {
        background-color: purple;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 10px;
    }
    .stTextInput input {
        font-size: 16px;
        text-align: center;
    }
    .stSelectbox select {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(emoji.emojize(":thinking_face: Number Guessing Game"))
st.subheader("Guess the number based on the selected difficulty!")

# Difficulty selection
difficulty = st.selectbox("🎮 Select Level", ["🟢 Easy", "🟡 Medium", "🔴 Hard"], index=["🟢 Easy", "🟡 Medium", "🔴 Hard"].index(st.session_state.difficulty))
if difficulty != st.session_state.difficulty:
    set_difficulty(difficulty)

st.markdown(f"**Current Level: {st.session_state.difficulty} {st.session_state.range}**")

# Input field for the user's guess
guess = st.number_input("🔢 Enter your guess:", min_value=1, max_value=200, step=1, value=st.session_state.guess if st.session_state.guess is not None else 1)
st.session_state.guess = guess

if st.button("✅ Submit Guess") and not st.session_state.game_over:
    st.session_state.attempts += 1
    st.session_state.remaining_attempts -= 1
    if st.session_state.guess < st.session_state.number:
        st.session_state.message = "📉 Too low! Try again."
    elif st.session_state.guess > st.session_state.number:
        st.session_state.message = "📈 Too high! Try again."
    else:
        st.session_state.message = f"🎉 Congratulations! You guessed the number in {st.session_state.attempts} attempts."
        st.session_state.game_over = True
    
    if st.session_state.remaining_attempts == 0 and not st.session_state.game_over:
        st.session_state.message = f"❌ Game Over! The correct number was {st.session_state.number}."
        st.session_state.game_over = True

st.markdown(f"**{st.session_state.message}**")

# Show remaining attempts
st.markdown(f"**⏳ Remaining Attempts: {st.session_state.remaining_attempts}**")

# Reset button to start a new game
if st.button("🔄 Reset Game"):
    set_difficulty(st.session_state.difficulty)
