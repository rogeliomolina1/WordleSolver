# solver.py
import os
import re
import nltk
from collections import Counter

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
    """
    raw_words = nltk.corpus.words.words()
    return sorted({w.lower() for w in raw_words if len(w) == 5 and w.isalpha()})

def score_words(words):
    """
    Rank words by letter frequency (unique letters weighted higher).
    """
    freq = Counter("".join(words))
    return sorted(words, key=lambda w: sum(freq[c] for c in set(w)), reverse=True)

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
