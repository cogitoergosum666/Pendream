import json

class Vocab:
    def __init__(self, filename="data/1000words.txt", dictionary_file="data/filtered.json"):
        
        self._file = filename
        self._dictionary_file = dictionary_file  # Path to the JSON dictionary file
        self._words = []
        self._word_dict = {}  # Dictionary to store word meanings, synonyms, and antonyms
        
        self.dictionary = {}  # Loaded dictionary from the JSON file

    @property
    def words(self):
        return self._words
    @property
    def word_dict(self):
        return self._word_dict


    def load_words(self):
        """Load words from the file, remove headings, and filter stopwords."""
        try:
            with open(self._file, "r") as file:
                for line in file:
                    # Skip empty lines and potential headings
                    line = line.strip()
                    if not line or any(char.isdigit() for char in line):  # Skip if contains digits (likely a heading)
                        continue
                    # Split words and filter out stopwords
                    words = line.split()
                    self._words.extend(words)
                self._words = sorted(list(set(self._words)))
        except FileNotFoundError:
            print(f"File '{self._file}' not found. No words will be loaded.")
        
    def words_dict(self):
        try:
            with open(self._dictionary_file, "r") as file:
                self.dictionary = json.load(file)
        except FileNotFoundError:
            print(f"Dictionary file '{self._dictionary_file}' not found. Please provide a valid JSON file.")
        except json.JSONDecodeError:
            print(f"Dictionary file '{self._dictionary_file}' is not a valid JSON file.")
        for word in self._words:
            word_upper = word.upper()
            entry = self.dictionary.get(word_upper)
            if entry:
                meanings = entry.get("MEANINGS", [])
                if meanings:  # Only add entries with non-empty meanings
                    self._word_dict[word] = {
                        "meanings": meanings,
                        # "synonyms": entry.get("SYNONYMS", []),
                        # "antonyms": entry.get("ANTONYMS", []),
                    }
                else:
                    # print(f"Word '{word}' not found in the dictionary.")
                    continue


