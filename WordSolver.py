import nltk
import re

def createWordList():
    # Download the required resources from NLTK
    nltk.download('words')

    # Load the word list
    words = nltk.corpus.words.words()
    five_letter_words = [word.lower() for word in words if len(word) == 5]

    # Sort words by popularity
    word_freq = nltk.FreqDist(five_letter_words)
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    return sorted_words

def filter_words_correct_letters(list, pattern):
  """Filters a list based on a regular expression pattern."""
  filtered_words = []
  for word in list:
    if re.match(pattern, word[0]):
      filtered_words.append(word[0])
  return filtered_words

def filter_words_incorrect_place_letters(words, letters):
  """Filters a list of words for words containing certain letters."""
  filtered_words = []
  for word in words:
    for letter in letters:
      if all(letter in word for letter in letters):
        filtered_words.append(word)
  return filtered_words

def filter_words_incorrect_letters(words,letters):
   filtered_words = []
   for word in words:
      if not any(letter in word for letter in letters):
        filtered_words.append(word)

   return filtered_words

def save_input_as_list_of_letters(input_string):
  """Saves an input as a list of letters when the input is comma and space separated."""
  list_of_letters = []
  for letter in input_string.split(','):
    list_of_letters.append(letter)
  return list_of_letters
    
def main():
    while(1):
        letter_list = []
        word_list = createWordList()
        guess = input("Welcome to Wordle Solver enter your what you have so far: ")
        while (len(guess) != 5):
            guess = input("Your guess needs to be 5 letters in length: ")
        pattern = '^'
        for letter in guess:
            if letter == '$':
                pattern += '[a-z]'
            else:
                letter_list.append(letter)
                pattern += letter
        pattern += '$' 
        incorrect_place_letter_input = input("Please enter the letters you don't know the correct place of: ")
        incorrect_place_letter_list = save_input_as_list_of_letters(incorrect_place_letter_input)
        incorrect_place_letter_list.extend(letter_list)
        print(incorrect_place_letter_list)
        filtered_words_correct_letters = []
        filtered_words_correct_letters = filter_words_correct_letters(word_list, pattern)
        filtered_words_incorrect_place = filter_words_incorrect_place_letters(filtered_words_correct_letters, incorrect_place_letter_list)
        incorrect_letter_input = input("Please enter the letters you know are incorrect: ")
        incorrect_letter_list = save_input_as_list_of_letters(incorrect_letter_input)
        final_filtered_words = filter_words_incorrect_letters(filtered_words_incorrect_place, incorrect_letter_list)
        for word in final_filtered_words:
            print(f"Word: {word}")
        if(len(final_filtered_words) <= 1):
           break

if __name__ == "__main__":
    main()