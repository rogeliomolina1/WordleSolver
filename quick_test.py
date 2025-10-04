#!/usr/bin/env python3
"""
Quick test runner for Wordle Solver.
Run this for fast testing during development.
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    """Run quick tests to verify basic functionality."""
    print("🚀 Quick Wordle Solver Test")
    print("=" * 40)
    
    try:
        from solver import load_word_list, solve
        
        # Test 1: Load words
        print("1️⃣ Testing word list loading...")
        words = load_word_list()
        print(f"   ✅ Loaded {len(words)} words")
        
        # Test 2: Check for important words
        print("2️⃣ Testing important words...")
        important_words = ['miaou', 'crane', 'slate', 'adieu', 'audio']
        found_words = [word for word in important_words if word in words]
        print(f"   ✅ Found {len(found_words)}/{len(important_words)} important words: {found_words}")
        
        # Test 3: Basic solving
        print("3️⃣ Testing basic solving...")
        results = solve('^.....$', [], [])
        print(f"   ✅ Found {len(results)} words for empty pattern")
        
        # Test 4: Pattern solving
        print("4️⃣ Testing pattern solving...")
        results = solve('^a....$', [], [])
        print(f"   ✅ Found {len(results)} words starting with 'a'")
        
        # Test 5: Constraint solving
        print("5️⃣ Testing constraint solving...")
        results = solve('^.....$', ['a', 'e'], ['x', 'z'])
        print(f"   ✅ Found {len(results)} words with constraints")
        
        # Test 6: Complex scenario
        print("6️⃣ Testing complex scenario...")
        results = solve('^a.e..$', ['o'], ['r', 't'])
        print(f"   ✅ Found {len(results)} words for complex pattern")
        
        print("\n🎉 All quick tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False

def test_specific_word(word):
    """Test if a specific word is in the word list."""
    try:
        from solver import load_word_list
        words = load_word_list()
        
        if word.lower() in words:
            print(f"✅ '{word}' is in the word list")
            return True
        else:
            print(f"❌ '{word}' is NOT in the word list")
            return False
    except Exception as e:
        print(f"❌ Error testing word '{word}': {e}")
        return False

def test_solve_scenario(pattern, must_contain=None, excluded=None):
    """Test a specific solving scenario."""
    try:
        from solver import solve
        
        results = solve(pattern, must_contain or [], excluded or [])
        print(f"Pattern: {pattern}")
        print(f"Must contain: {must_contain}")
        print(f"Excluded: {excluded}")
        print(f"Results: {len(results)} words")
        print(f"Top 5: {results[:5]}")
        return True
    except Exception as e:
        print(f"❌ Error testing scenario: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "word" and len(sys.argv) > 2:
            # Test specific word
            word = sys.argv[2]
            test_specific_word(word)
        elif command == "solve" and len(sys.argv) > 2:
            # Test specific solve scenario
            pattern = sys.argv[2]
            must_contain = sys.argv[3].split(',') if len(sys.argv) > 3 and sys.argv[3] else []
            excluded = sys.argv[4].split(',') if len(sys.argv) > 4 and sys.argv[4] else []
            test_solve_scenario(pattern, must_contain, excluded)
        else:
            print("Usage:")
            print("  python quick_test.py                    # Run all quick tests")
            print("  python quick_test.py word MIAOU         # Test specific word")
            print("  python quick_test.py solve '^a....$' a,e x,z  # Test solve scenario")
    else:
        # Run all quick tests
        success = quick_test()
        sys.exit(0 if success else 1)
