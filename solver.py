# solver.py
import os
import re
import nltk
from collections import Counter
import wordfreq

# --- Configure local NLTK data directory ---
BASE_DIR = os.path.dirname(__file__)
NLTK_DATA_DIR = os.path.join(BASE_DIR, "nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

# Make sure our custom dir is first in the search path
if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.insert(0, NLTK_DATA_DIR)

# --- Ensure corpus is available ---
try:
    nltk.corpus.words.words()
except LookupError:
    # Download to the local project folder
    nltk.download("words", download_dir=NLTK_DATA_DIR)

# ---------- Core Functions ----------

def load_word_list():
    """
    Return list of all 5-letter English words (lowercase).
    Uses multiple sources for comprehensive coverage including Wordle-specific words.
    """
    # Get words from NLTK
    nltk_words = {w.lower() for w in nltk.corpus.words.words() if len(w) == 5 and w.isalpha()}
    
    # Get common 5-letter words from wordfreq
    wordfreq_words = set()
    try:
        # Get comprehensive word list from wordfreq
        common_words = wordfreq.get_frequency_dict('en', wordlist='large')
        wordfreq_words = {w.lower() for w in common_words.keys() if len(w) == 5 and w.isalpha()}
    except:
        pass  # Fallback to NLTK only if wordfreq fails
    
    # Add some additional Wordle-specific words that might be missing
    additional_words = {
        'miaou', 'miaow', 'miaul', 'miaul', 'miaow', 'miaou',  # cat sounds
        'qajaq', 'qanat', 'qapik', 'qibla', 'qophs', 'qorma',  # Q words
        'xenon', 'xylem', 'xerox', 'xeric', 'xenon',  # X words
        'zebra', 'zesty', 'zilch', 'zonal', 'zoned',  # Z words
        'fjord', 'fjeld', 'fjall',  # Fj words
        'cwtch', 'crwth', 'cwtch',  # Welsh words
        'pygmy', 'pzazz', 'pzazz',  # P words
        'vying', 'vying', 'vying',  # V words
        'jumbo', 'jumpy', 'jumpy',  # J words
        'kayak', 'kayak', 'kayak',  # K words
        'waltz', 'waltz', 'waltz',  # W words
        'yacht', 'yacht', 'yacht',  # Y words
        'zebra', 'zebra', 'zebra',  # Z words
        'audio', 'audio', 'audio',  # A words
        'eerie', 'eerie', 'eerie',  # E words
        'ouija', 'ouija', 'ouija',  # O words
        'queue', 'queue', 'queue',  # Q words
        'pizza', 'pizza', 'pizza',  # P words
        'jazzy', 'jazzy', 'jazzy',  # J words
        'fuzzy', 'fuzzy', 'fuzzy',  # F words
        'buzzy', 'buzzy', 'buzzy',  # B words
        'hazel', 'hazel', 'hazel',  # H words
        'mazel', 'mazel', 'mazel',  # M words
        'razor', 'razor', 'razor',  # R words
        'major', 'major', 'major',  # M words
        'minor', 'minor', 'minor',  # M words
        'motor', 'motor', 'motor',  # M words
        'color', 'color', 'color',  # C words
        'favor', 'favor', 'favor',  # F words
        'labor', 'labor', 'labor',  # L words
        'humor', 'humor', 'humor',  # H words
        'rumor', 'rumor', 'rumor',  # R words
        'tumor', 'tumor', 'tumor',  # T words
        'vigor', 'vigor', 'vigor',  # V words
        'error', 'error', 'error',  # E words
        'mirror', 'mirror', 'mirror',  # M words (6 letters, but common)
        'terror', 'terror', 'terror',  # T words (6 letters, but common)
        'horror', 'horror', 'horror',  # H words (6 letters, but common)
    }
    
    # Filter additional words to only 5-letter words
    additional_words = {w for w in additional_words if len(w) == 5}
    
    # Combine all sources
    all_words = nltk_words.union(wordfreq_words).union(additional_words)
    return sorted(all_words)

def score_words(words):
    """
    Rank words by frequency (common words first) and letter frequency.
    """
    def word_score(word):
        # Get word frequency (higher is more common)
        freq_score = wordfreq.word_frequency(word, 'en')
        # Bonus for unique letters
        unique_letters = len(set(word))
        return freq_score + (unique_letters * 0.01)
    
    return sorted(words, key=word_score, reverse=True)

def solve(pattern, must_contain=None, excluded=None):
    """
    Filter & rank candidate words.

    pattern      -> regex like '^a..le$'
    must_contain -> list of letters that must be present
    excluded     -> list of letters that cannot be present
    """
    must_contain = must_contain or []
    excluded = excluded or []

    words = load_word_list()
    regex = re.compile(pattern)

    candidates = [w for w in words if regex.match(w)]

    if must_contain:
        candidates = [w for w in candidates if all(ch in w for ch in must_contain)]

    if excluded:
        candidates = [w for w in candidates if all(ch not in w for ch in excluded)]

    return score_words(candidates)
