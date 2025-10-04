# 🟩 Collaborative Wordle Solver

A smart collaborative Wordle solver that works with you to solve Wordle puzzles! Enter your guesses, mark the results, and get intelligent suggestions for your next move. The AI tracks all your guesses and progressively narrows down the possibilities.

## ✨ Features

- **🤝 Collaborative Solving**: Work together with AI - enter guesses, get suggestions, repeat!
- **📊 Progressive Tracking**: AI remembers all your guesses and constraints
- **🎯 Smart Suggestions**: Get suggestions after every guess, not just at the end
- **📚 Comprehensive Word List**: Includes 42,000+ words including Wordle-specific words like "miaou"
- **🧠 Intelligent Scoring**: Prioritizes common words using real-world frequency data
- **📈 Real-time Constraints**: See current green, yellow, and gray letters at a glance
- **🔄 Easy Reset**: Start over anytime with the reset button
- **✅ Input Validation**: Validates guesses and provides helpful feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/WordleSolver.git
   cd WordleSolver
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🎮 How to Use

1. **Enter your 5-letter guess** in the text input
2. **Click each letter** to cycle through colors:
   - ⬜ **Gray**: Letter not in the word
   - 🟨 **Yellow**: Letter is in the word but wrong position  
   - 🟩 **Green**: Letter is correct and in the right position
3. **Click "Add Guess & Get Suggestions"** to save your guess and get AI suggestions
4. **Repeat the process** - the AI tracks all your guesses and gives better suggestions each time
5. **Use "Reset"** to start over

## 🧠 How It Works

The collaborative solver uses a sophisticated algorithm that:

1. **Tracks all guesses** and builds a complete constraint model
2. **Filters words** based on all your green, yellow, and gray feedback
3. **Scores words** using real-world frequency data from the `wordfreq` library
4. **Prioritizes common words** that are more likely to be the answer
5. **Considers letter uniqueness** to maximize information gain
6. **Updates suggestions** after every guess to help you narrow down possibilities

## 📁 Project Structure

```
WordleSolver/
├── app.py              # Streamlit web application
├── solver.py           # Core solving logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore rules
└── nltk_data/         # Local NLTK data (auto-created)
```

## 🔧 Technical Details

- **Word Sources**: Combines NLTK's English word corpus with wordfreq's frequency data
- **Scoring Algorithm**: Uses word frequency + letter uniqueness bonus
- **Performance**: Cached word loading for fast suggestions
- **Dependencies**: Streamlit, NLTK, wordfreq

## 📝 Notes

- The first run will download the NLTK words corpus into a local `nltk_data/` folder
- The `nltk_data/` folder is excluded from Git with `.gitignore`
- The app loads ~42,000 five-letter words including Wordle-specific words like "miaou", "qajaq", "fjord"
- This is a **collaborative solver** - it works with you step by step, not a one-shot solution