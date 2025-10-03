import streamlit as st
from solver import load_word_list, solve

# Load words once
WORDS = load_word_list()

st.set_page_config(page_title="Wordle Solver", page_icon="🟩", layout="centered")

st.title("🟩 Wordle Solver")
st.write("Enter your guess and mark letters as green (🟩), yellow (🟨), or gray (⬜).")

# State
if "guesses" not in st.session_state:
    st.session_state.guesses = []

# Input for guess
guess = st.text_input("Enter your 5-letter guess:", "").lower()

if guess and len(guess) == 5 and guess.isalpha():
    colors = []
    st.write("Click to mark each letter's status:")
    cols = st.columns(5)

    for i, letter in enumerate(guess):
        if f"color_{i}" not in st.session_state:
            st.session_state[f"color_{i}"] = "⬜"

        def cycle_color(i=i):
            current = st.session_state[f"color_{i}"]
            if current == "⬜":
                st.session_state[f"color_{i}"] = "🟨"
            elif current == "🟨":
                st.session_state[f"color_{i}"] = "🟩"
            else:
                st.session_state[f"color_{i}"] = "⬜"

        cols[i].button(
            f"{letter.upper()} {st.session_state[f'color_{i}']}",
            key=f"btn_{i}",
            on_click=cycle_color
        )
        colors.append(st.session_state[f"color_{i}"])

    if st.button("Add Guess"):
        st.session_state.guesses.append((guess, colors))

# Display guesses
for g, c in st.session_state.guesses:
    st.write("".join([f"{letter.upper()} {color}" for letter, color in zip(g, c)]))

# Process all guesses and solve
if st.button("Solve"):
    pattern = ["?"] * 5
    yellow_letters = []
    gray_letters = []

    for g, c in st.session_state.guesses:
        for i, (letter, color) in enumerate(zip(g, c)):
            if color == "🟩":  # green
                pattern[i] = letter
            elif color == "🟨":  # yellow
                yellow_letters.append(letter)
            elif color == "⬜":  # gray
                gray_letters.append(letter)

    pattern = "".join(pattern)
    results = solve(pattern, yellow_letters, gray_letters, WORDS)

    if results:
        st.success(f"Found {len(results)} possible words.")
        st.write("### Top Suggestions")
        st.write(", ".join(results[:20]))
    else:
        st.error("No words found. Check your inputs!")
