import streamlit as st
from solver import load_word_list, solve

# Load words once with caching
@st.cache_data
def get_words():
    return load_word_list()

WORDS = get_words()

st.set_page_config(page_title="Wordle Solver", page_icon="🟩", layout="centered")

st.title("🟩 Collaborative Wordle Solver")
st.markdown("**Work together with the AI to solve Wordle! Enter your guess, mark the results, and get smart suggestions for your next move.**")

# Instructions
with st.expander("📖 How to use"):
    st.markdown("""
    1. **Enter your 5-letter guess** in the text box below
    2. **Click each letter** to cycle through colors:
       - ⬜ Gray: Letter not in the word
       - 🟨 Yellow: Letter is in the word but wrong position  
       - 🟩 Green: Letter is correct and in the right position
    3. **Click "Add Guess"** to save your guess and get suggestions
    4. **The AI will track all your guesses** and give you the best next suggestions
    5. **Use "Reset"** to start over
    """)

st.markdown("---")

# Initialize session state
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "current_suggestions" not in st.session_state:
    st.session_state.current_suggestions = []

# Show current game state
if st.session_state.guesses:
    st.markdown("### 🎯 Current Game State")
    
    # Display all guesses
    for i, (g, c) in enumerate(st.session_state.guesses):
        st.write(f"**Guess {i+1}:** " + "".join([f"{letter.upper()} {color}" for letter, color in zip(g, c)]))
    
    # Show current constraints
    st.markdown("#### 📊 Current Constraints:")
    
    # Analyze current state
    pattern = ["."] * 5
    yellow_letters = []
    gray_letters = []
    green_positions = {}

    for g, c in st.session_state.guesses:
        for i, (letter, color) in enumerate(zip(g, c)):
            if color == "🟩":  # green
                pattern[i] = letter
                green_positions[i] = letter
            elif color == "🟨":  # yellow
                yellow_letters.append(letter)
            elif color == "⬜":  # gray
                gray_letters.append(letter)

    # Remove duplicates and show constraints
    yellow_letters = list(set(yellow_letters))
    gray_letters = list(set(gray_letters))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Green Letters", len(green_positions))
    with col2:
        st.metric("Yellow Letters", len(yellow_letters))
    with col3:
        st.metric("Gray Letters", len(gray_letters))
    
    if green_positions:
        st.write(f"**Known positions:** {dict(green_positions)}")
    if yellow_letters:
        st.write(f"**Must contain:** {', '.join(yellow_letters).upper()}")
    if gray_letters:
        st.write(f"**Cannot contain:** {', '.join(gray_letters).upper()}")
    
    st.markdown("---")

# Input for new guess
st.markdown("### 🎮 Make Your Next Guess")
guess = st.text_input("Enter your 5-letter guess:", "", max_chars=5).lower()

# Validate guess
if guess:
    if len(guess) != 5:
        st.error("Please enter exactly 5 letters.")
    elif not guess.isalpha():
        st.error("Please enter only letters.")
    elif guess not in WORDS:
        st.warning(f"'{guess.upper()}' is not in our word list, but you can still use it.")

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

    if st.button("Add Guess & Get Suggestions"):
        # Add the guess
        st.session_state.guesses.append((guess, colors))
        
        # Clear color states for next guess
        for i in range(5):
            if f"color_{i}" in st.session_state:
                del st.session_state[f"color_{i}"]
        
        # Get suggestions
        pattern = ["."] * 5
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

        # Convert pattern to regex format
        pattern_regex = "^" + "".join(pattern) + "$"
        results = solve(pattern_regex, yellow_letters, gray_letters)
        st.session_state.current_suggestions = results
        
        st.rerun()

# Show suggestions
if st.session_state.current_suggestions:
    st.markdown("### 💡 AI Suggestions for Next Guess")
    
    results = st.session_state.current_suggestions
    
    if results:
        st.success(f"🎯 Found {len(results)} possible words!")
        
        # Display top 10 suggestions in a nice format
        for i, word in enumerate(results[:10], 1):
            st.write(f"**{i}.** {word.upper()}")
        
        if len(results) > 10:
            st.info(f"Showing top 10 of {len(results)} suggestions. Try these common words first!")
        
        # Show some statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Matches", len(results))
        with col2:
            st.metric("Top Suggestion", results[0].upper())
        with col3:
            st.metric("Unique Letters", len(set(results[0])))
        
        # Show if we're getting close
        if len(results) <= 5:
            st.success("🎉 You're getting close! Only a few possibilities left!")
        elif len(results) <= 20:
            st.info("🔍 Good progress! Narrowing down the possibilities.")
    else:
        st.error("❌ No words found! Check your inputs or try a different approach.")

# Reset button
if st.button("🔄 Reset Game"):
    st.session_state.guesses = []
    st.session_state.current_suggestions = []
    for i in range(5):
        if f"color_{i}" in st.session_state:
            del st.session_state[f"color_{i}"]
    st.rerun()
