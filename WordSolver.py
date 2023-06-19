import nltk

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
    
def main():

    word_list = createWordList()

    # Print a sample of the first 10 words
    print("Sample of the first 10 words:")
    for word, frequency in word_list[:10]:
        print(f"Word: {word}, Frequency: {frequency}")

if __name__ == "__main__":
    main()