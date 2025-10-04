import streamlit as st
from solver import load_word_list, solve

# Load words with cache busting
import time
WORDS = load_word_list()
st.sidebar.write(f"Word list loaded at: {time.strftime('%H:%M:%S')}")
st.sidebar.write(f"Total words: {len(WORDS)}")
st.sidebar.write(f"Contains 'miaou': {'miaou' in WORDS}")

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
if "game_won" not in st.session_state:
    st.session_state.game_won = False
if "enter_pressed" not in st.session_state:
    st.session_state.enter_pressed = False

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
        st.write(f"**Must contain:** {', '.join([l.upper() for l in yellow_letters])}")
    if gray_letters:
        st.write(f"**Cannot contain:** {', '.join([l.upper() for l in gray_letters])}")
    
    st.markdown("---")

# Input for new guess
st.markdown("### 🎮 Make Your Next Guess")

# Initialize input state
if "input_guess" not in st.session_state:
    st.session_state.input_guess = ""

# Use session state for the input with on_change callback
def on_input_change():
    st.session_state.input_guess = st.session_state.guess_input.upper()

guess = st.text_input("Enter your 5-letter guess:", value=st.session_state.input_guess, max_chars=5, key="guess_input", on_change=on_input_change).upper()

# Update session state when input changes
if guess != st.session_state.input_guess:
    st.session_state.input_guess = guess

# Validate guess
if guess:
    if len(guess) != 5:
        st.error("Please enter exactly 5 letters.")
    elif not guess.isalpha():
        st.error("Please enter only letters.")
    elif guess.lower() not in WORDS:
        # Debug information
        st.warning(f"'{guess}' is not in our word list, but you can still use it.")
        with st.expander("Debug Info"):
            st.write(f"Total words loaded: {len(WORDS)}")
            st.write(f"Looking for: '{guess.lower()}'")
            st.write(f"Found: {guess.lower() in WORDS}")
            st.write(f"Words starting with '{guess.lower()[:3]}': {[w for w in WORDS if w.startswith(guess.lower()[:3])]}")

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
            f"{letter} {st.session_state[f'color_{i}']}",
            key=f"btn_{i}",
            on_click=cycle_color
        )
        colors.append(st.session_state[f"color_{i}"])

    # Create a form for the entire guess section to handle Enter key
    with st.form("guess_form"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit_button = st.form_submit_button("Add Guess & Get Suggestions")
        
        with col2:
            clear_button = st.form_submit_button("Clear Input")
    
    # Handle form submission
    if submit_button:
        # Add the guess (convert to lowercase for processing)
        st.session_state.guesses.append((guess.lower(), colors))
        
        # Check if all letters are green (WIN!)
        all_green = all(color == "🟩" for color in colors)
        if all_green:
            st.session_state.game_won = True
            st.session_state.winning_word = guess.upper()
        
        # Clear color states for next guess
        for i in range(5):
            if f"color_{i}" in st.session_state:
                del st.session_state[f"color_{i}"]
        
        # Clear the input field immediately
        st.session_state.input_guess = ""
        
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
    
    elif clear_button:
        st.session_state.input_guess = ""
        for i in range(5):
            if f"color_{i}" in st.session_state:
                del st.session_state[f"color_{i}"]
        st.rerun()
    
    # Add Enter key support
    st.markdown("💡 **Tip:** Press Enter to submit your guess!")
    
    # Debug info
    with st.expander("🔍 Debug Info"):
        st.write(f"Current input: '{st.session_state.input_guess}'")
        st.write(f"Current guess: '{guess}'")
        st.write(f"Game won: {st.session_state.game_won}")
        st.write(f"Number of guesses: {len(st.session_state.guesses)}")

# Show suggestions
if st.session_state.current_suggestions:
    st.markdown("### 💡 AI Suggestions for Next Guess")
    
    results = st.session_state.current_suggestions
    
    if results:
        st.success(f"🎯 Found {len(results)} possible words!")
        
        # Display top 10 suggestions with clickable buttons
        st.markdown("**Click a suggestion to use it as your next guess:**")
        
        # Create columns for suggestions
        cols = st.columns(2)
        for i, word in enumerate(results[:10]):
            col_idx = i % 2
            with cols[col_idx]:
                if st.button(f"{word.upper()}", key=f"suggestion_{i}", help=f"Use {word.upper()} as your next guess"):
                    # Update the input guess
                    st.session_state.input_guess = word.upper()
                    # Clear color states when selecting a suggestion
                    for j in range(5):
                        if f"color_{j}" in st.session_state:
                            del st.session_state[f"color_{j}"]
                    # Force a rerun to update the input field
                    st.rerun()
        
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

# Show celebration if game is won
if st.session_state.game_won:
    st.balloons()
    st.success(f"🎉🎉🎉 CONGRATULATIONS! 🎉🎉🎉")
    st.success(f"You solved it! The word was: **{st.session_state.winning_word}**")
    st.success(f"You solved it in {len(st.session_state.guesses)} guesses!")
    
    # Show final game state
    st.markdown("### 🏆 Final Game State")
    for i, (g, c) in enumerate(st.session_state.guesses):
        st.write(f"**Guess {i+1}:** " + "".join([f"{letter.upper()} {color}" for letter, color in zip(g, c)]))

# Reset button
if st.button("🔄 Reset Game"):
    st.session_state.guesses = []
    st.session_state.current_suggestions = []
    st.session_state.input_guess = ""
    st.session_state.game_won = False
    st.session_state.winning_word = ""
    for i in range(5):
        if f"color_{i}" in st.session_state:
            del st.session_state[f"color_{i}"]
    st.rerun()
