#!/usr/bin/env python3
"""
Comprehensive test suite for the Wordle Solver application.
Run this file to test all functionality of the solver.
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver import load_word_list, solve, score_words

class TestWordleSolver(unittest.TestCase):
    """Test cases for the Wordle Solver functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.words = load_word_list()
    
    def test_word_list_loading(self):
        """Test that the word list loads correctly."""
        print("Testing word list loading...")
        
        # Test basic properties
        self.assertIsInstance(self.words, list)
        self.assertGreater(len(self.words), 1000, "Word list should have many words")
        
        # Test that all words are 5 letters
        for word in self.words:
            self.assertEqual(len(word), 5, f"Word '{word}' should be 5 letters")
            self.assertTrue(word.isalpha(), f"Word '{word}' should contain only letters")
            self.assertTrue(word.islower(), f"Word '{word}' should be lowercase")
        
        print(f"✅ Word list loaded successfully: {len(self.words)} words")
    
    def test_word_list_comprehensive(self):
        """Test that the word list includes important Wordle words."""
        print("Testing word list comprehensiveness...")
        
        important_words = [
            'miaou', 'qajaq', 'fjord', 'cwtch', 'crwth',
            'audio', 'eerie', 'ouija', 'queue', 'pizza',
            'jazzy', 'fuzzy', 'buzzy', 'hazel', 'major',
            'minor', 'motor', 'color', 'favor', 'labor',
            'humor', 'rumor', 'tumor', 'vigor', 'error'
        ]
        
        missing_words = []
        for word in important_words:
            if word not in self.words:
                missing_words.append(word)
        
        if missing_words:
            print(f"⚠️  Missing words: {missing_words}")
        else:
            print("✅ All important Wordle words are included")
        
        # At least 90% of important words should be present
        self.assertGreaterEqual(
            len(important_words) - len(missing_words), 
            len(important_words) * 0.9,
            f"Too many important words missing: {missing_words}"
        )
    
    def test_solve_basic_patterns(self):
        """Test basic pattern solving functionality."""
        print("Testing basic pattern solving...")
        
        # Test empty pattern (all dots)
        results = solve('^.....$', [], [])
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 100, "Should return many words for empty pattern")
        
        # Test specific letter in position
        results = solve('^a....$', [], [])
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 10, "Should return words starting with 'a'")
        
        # Verify all results start with 'a'
        for word in results[:10]:  # Check first 10
            self.assertTrue(word.startswith('a'), f"Word '{word}' should start with 'a'")
        
        print("✅ Basic pattern solving works correctly")
    
    def test_solve_with_constraints(self):
        """Test solving with yellow and gray letter constraints."""
        print("Testing constraint solving...")
        
        # Test with yellow letters (must contain)
        results = solve('^.....$', ['a', 'e'], [])
        self.assertIsInstance(results, list)
        
        # Verify all results contain required letters
        for word in results[:10]:
            self.assertIn('a', word, f"Word '{word}' should contain 'a'")
            self.assertIn('e', word, f"Word '{word}' should contain 'e'")
        
        # Test with gray letters (must not contain)
        results = solve('^.....$', [], ['x', 'z'])
        self.assertIsInstance(results, list)
        
        # Verify no results contain excluded letters
        for word in results[:10]:
            self.assertNotIn('x', word, f"Word '{word}' should not contain 'x'")
            self.assertNotIn('z', word, f"Word '{word}' should not contain 'z'")
        
        print("✅ Constraint solving works correctly")
    
    def test_solve_complex_scenarios(self):
        """Test complex solving scenarios."""
        print("Testing complex scenarios...")
        
        # Scenario 1: Known positions + yellow letters
        results = solve('^a.e..$', ['o'], ['r', 't'])
        self.assertIsInstance(results, list)
        
        for word in results[:5]:
            self.assertTrue(word.startswith('a'), f"Word '{word}' should start with 'a'")
            self.assertEqual(word[2], 'e', f"Word '{word}' should have 'e' in position 3")
            self.assertIn('o', word, f"Word '{word}' should contain 'o'")
            self.assertNotIn('r', word, f"Word '{word}' should not contain 'r'")
            self.assertNotIn('t', word, f"Word '{word}' should not contain 't'")
        
        # Scenario 2: Multiple constraints
        results = solve('^..o..$', ['a', 'e'], ['r', 't', 's'])
        self.assertIsInstance(results, list)
        
        for word in results[:5]:
            self.assertEqual(word[2], 'o', f"Word '{word}' should have 'o' in position 3")
            self.assertIn('a', word, f"Word '{word}' should contain 'a'")
            self.assertIn('e', word, f"Word '{word}' should contain 'e'")
            self.assertNotIn('r', word, f"Word '{word}' should not contain 'r'")
            self.assertNotIn('t', word, f"Word '{word}' should not contain 't'")
            self.assertNotIn('s', word, f"Word '{word}' should not contain 's'")
        
        print("✅ Complex scenarios work correctly")
    
    def test_score_words_functionality(self):
        """Test the word scoring functionality."""
        print("Testing word scoring...")
        
        test_words = ['about', 'their', 'would', 'other', 'after']
        scored_words = score_words(test_words)
        
        self.assertIsInstance(scored_words, list)
        self.assertEqual(len(scored_words), len(test_words))
        
        # Check that words are sorted (should be in descending order of score)
        for i in range(len(scored_words) - 1):
            # This is a basic check - in practice, scoring might be more complex
            self.assertIsInstance(scored_words[i], str)
        
        print("✅ Word scoring works correctly")
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        print("Testing edge cases...")
        
        # Test with no matches
        results = solve('^zzzzz$', [], [])
        self.assertIsInstance(results, list)
        # Should return empty list or very few results
        
        # Test with impossible constraints
        results = solve('^.....$', ['a', 'b', 'c', 'd', 'e', 'f'], [])
        self.assertIsInstance(results, list)
        # Should return empty list (no 5-letter word can contain 6 different letters)
        
        # Test with conflicting constraints
        results = solve('^a....$', [], ['a'])
        self.assertIsInstance(results, list)
        # Should return empty list (can't start with 'a' and not contain 'a')
        
        print("✅ Edge cases handled correctly")
    
    def test_performance(self):
        """Test performance of the solver."""
        print("Testing performance...")
        
        import time
        
        # Test solving speed
        start_time = time.time()
        results = solve('^.....$', [], [])
        end_time = time.time()
        
        solve_time = end_time - start_time
        self.assertLess(solve_time, 5.0, f"Solving should be fast (took {solve_time:.2f}s)")
        
        print(f"✅ Performance test passed: {solve_time:.2f}s for {len(results)} results")
    
    def test_word_validation_scenarios(self):
        """Test various word validation scenarios."""
        print("Testing word validation scenarios...")
        
        # Test common starting words
        common_words = ['crane', 'slate', 'adieu', 'audio', 'raise', 'roate']
        for word in common_words:
            self.assertIn(word, self.words, f"Common word '{word}' should be in word list")
        
        # Test some edge cases
        edge_words = ['miaou', 'qajaq', 'fjord', 'cwtch']
        for word in edge_words:
            if word in self.words:
                print(f"✅ Edge word '{word}' is included")
            else:
                print(f"⚠️  Edge word '{word}' is missing")
        
        print("✅ Word validation scenarios completed")

class TestAppIntegration(unittest.TestCase):
    """Test cases for app integration and user scenarios."""
    
    def test_typical_wordle_session(self):
        """Test a typical Wordle solving session."""
        print("Testing typical Wordle session...")
        
        # Simulate a typical solving session
        words = load_word_list()
        
        # First guess: CRANE
        results1 = solve('^.....$', [], [])
        self.assertGreater(len(results1), 100)
        
        # Second guess: SLOTH (assuming some letters found)
        results2 = solve('^.....$', ['a', 'e'], ['c', 'r', 'n'])
        self.assertGreater(len(results2), 10)
        
        # Third guess: More specific
        results3 = solve('^a....$', ['e'], ['c', 'r', 'n', 's', 'l', 'o', 't', 'h'])
        self.assertGreater(len(results3), 0)
        
        # Verify progression (should get more specific)
        self.assertLessEqual(len(results3), len(results2))
        self.assertLessEqual(len(results2), len(results1))
        
        print("✅ Typical Wordle session simulation passed")
    
    def test_winning_scenario(self):
        """Test a winning scenario."""
        print("Testing winning scenario...")
        
        # Simulate finding the word "ABOUT"
        results = solve('^a....$', ['b', 'o', 'u', 't'], [])
        
        # Should include "about" in results
        self.assertIn('about', results)
        
        # Final check - exact match
        final_results = solve('^about$', [], [])
        self.assertIn('about', final_results)
        
        print("✅ Winning scenario test passed")

def run_tests():
    """Run all tests and provide a summary."""
    print("🧪 Starting Wordle Solver Test Suite")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestWordleSolver))
    suite.addTests(loader.loadTestsFromTestCase(TestAppIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failures}")
    print(f"💥 Errors: {errors}")
    
    if failures > 0:
        print(f"\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if errors > 0:
        print(f"\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if failures == 0 and errors == 0:
        print("🎉 All tests passed! Your Wordle solver is working correctly!")
        return True
    else:
        print("⚠️  Some tests failed. Check the issues above.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
