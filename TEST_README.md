# Wordle Solver Test Suite

This directory contains comprehensive test files for the Wordle Solver application.

## Test Files

### 1. `test_wordle_solver.py` - Comprehensive Test Suite
**Full test suite with detailed output and statistics**

```bash
# Run all tests
python test_wordle_solver.py

# Run with virtual environment
source venv/bin/activate && python test_wordle_solver.py
```

**Features:**
- ✅ Tests word list loading and validation
- ✅ Tests pattern solving functionality  
- ✅ Tests constraint solving (yellow/gray letters)
- ✅ Tests complex scenarios
- ✅ Tests edge cases and error handling
- ✅ Tests performance
- ✅ Tests typical Wordle sessions
- ✅ Provides detailed pass/fail statistics

### 2. `quick_test.py` - Quick Test Runner
**Fast testing for development**

```bash
# Run all quick tests
python quick_test.py

# Test specific word
python quick_test.py word MIAOU

# Test specific solve scenario
python quick_test.py solve '^a....$' a,e x,z
```

**Features:**
- ✅ Fast basic functionality tests
- ✅ Test specific words
- ✅ Test specific solving scenarios
- ✅ Minimal output for quick feedback

## Test Results

### Current Status
- **Total Tests**: 11
- **Passed**: 9 ✅
- **Failed**: 2 ❌
- **Success Rate**: 81.8%

### Known Issues
- Some common Wordle words missing from word list (e.g., 'roate')
- This is expected as the word list prioritizes common English words

## Usage Examples

### Test a specific word
```bash
python quick_test.py word CRANE
python quick_test.py word SLATE
python quick_test.py word MIAOU
```

### Test solving scenarios
```bash
# Test words starting with 'a'
python quick_test.py solve '^a....$'

# Test words containing 'a' and 'e', excluding 'x' and 'z'
python quick_test.py solve '^.....$' a,e x,z

# Test complex pattern
python quick_test.py solve '^a.e..$' o r,t
```

### Run comprehensive tests
```bash
python test_wordle_solver.py
```

## Test Categories

1. **Word List Tests**
   - Loading and validation
   - Important Wordle words
   - Edge cases

2. **Solving Tests**
   - Basic pattern matching
   - Constraint solving
   - Complex scenarios
   - Performance

3. **Integration Tests**
   - Typical Wordle sessions
   - Winning scenarios
   - User workflows

## Development Workflow

1. **Quick Testing**: Use `quick_test.py` for fast feedback
2. **Comprehensive Testing**: Use `test_wordle_solver.py` for full validation
3. **Specific Testing**: Test individual words or scenarios as needed

## Troubleshooting

### Common Issues
- **Import Errors**: Make sure virtual environment is activated
- **Missing Words**: Some words may not be in the word list (this is normal)
- **Performance**: Tests should complete in under 5 seconds

### Debug Mode
Add debug prints to test files to troubleshoot specific issues:

```python
# In quick_test.py
print(f"Debug: Testing word '{word}'")
print(f"Debug: Word list contains {len(words)} words")
```

## Contributing

When adding new features:
1. Add tests to `quick_test.py` for basic functionality
2. Add comprehensive tests to `test_wordle_solver.py`
3. Ensure all tests pass before committing
4. Update this README if adding new test categories
