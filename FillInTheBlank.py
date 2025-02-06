"""class FillInTheBlank"""
from random import randint, choice, sample
from Question import Question
# from Vocab import Vocab

class FillInTheBlank(Question):
    """
    This class generates fill-in-the-blank questions from a vocabulary list. Words are masked partially and randomly,
    leaving the first and last letters intact, and blanks are represented with '_'. 
    Example: 'hello' -> 'h__lo' with the answer 'el'.
    """

    def __init__(self, vocab_lib) -> None:
        super().__init__()
        self._vocab_library = vocab_lib  # Vocabulary library (JSON-like dictionary)
        self._used_words = set()

    @property
    def question(self):
        return self._question

    @property
    def answer(self):
        return {q: ans for q, ans in self._question_set.items()}

    @property
    def vocab_library(self):
        return self._vocab_library

    @vocab_library.setter
    def vocab_library(self, aVocabBook):
        # Accepts a pre-processed vocabulary dictionary
        self._vocab_library = aVocabBook

    def generate_question(self,difficulty):
        """
        Automatically generates fill-in-the-blank questions.
        Selects words from the vocabulary and masks some letters.
        """
        if not self._vocab_library:
            raise ValueError("Vocabulary library is empty. Please set vocab_library before generating questions.")
        
        # Randomly select a word from the vocabulary
        available_words = {word for word in self._vocab_library.keys() if len(word) > 2} - self._used_words
        print(available_words)
        # Randomly select a word that hasn't been used yet
        if not available_words or available_words == {}:
            # print("No more words available for question generation. Stopping...")
            return None
        num_blanks = 1
        word = choice(list(available_words))
        self._used_words.add(word)
        definition = self._vocab_library[word].get("meanings", [["No definition available"]])[0][1]
        max_blanks = len(word) - 2
        if difficulty == 1:
        # Generate the fill-in-the-blank format based on the word's length
            if len(word) == 3:
                num_blanks = 1
            elif len(word) == 4:
                num_blanks = 2
            else:
                # Mask random positions between the first and last letters for words longer than 4
                num_blanks = randint(1,2)  # Random number of blanks
        elif difficulty == 2:
            num_blanks = 3
        elif difficulty == 3:
            num_blanks = randint(4,len(word) - 2)

        indices_to_blank = sorted(sample(range(1, len(word) - 1), num_blanks))
        question = list(word)
        answer = []
        for idx in indices_to_blank:
            answer.append(question[idx])
            question[idx] = '_'
        question = ''.join(question)
        answer = ''.join(answer)
        
        # Save the generated question and answer
        self._question = (question,definition,difficulty)
        self._answer = answer
        

    def _is_question_exist(self, question) -> bool:
        """
        Checks if a question already exists in the question set.
        """
        return question in self._question_set.keys()

    def add_question(self):
        """
        Adds the current question and answer pair to the question set.
        (This method can be expanded if manual question addition is required.)
        """
        if not self._is_question_exist(self._question):
            self._question_set[self._question] = self._answer
# testing part

# if __name__ == "__main__":
#     vocab = {
#         "a": {"meanings": [["letter", "The first letter of the alphabet"]]},
#         "ok": {"meanings": [["adjective", "Used to express agreement or acceptance"]]},
#     }
#     fill_in_the_blank = FillInTheBlank(vocab)
#     fill_in_the_blank.generate_question(difficulty=1)
#     print(fill_in_the_blank.question_set)
