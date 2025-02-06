import random
from Vocab import Vocab
from FillInTheBlank import FillInTheBlank

class Question_set:

    def __init__(self, type = '1000words', len1 = 5, difficulty = 1) -> None:
        '''
        the word type range from (1000words, nouns, verbs, and adjectives_adverbs)
        len1 is the len of the questions set
        '''
        if type == 'Mix' or type == 'mix':
            type = '1000words'
        elif type == "Adjectives/Adverbs":
            type = 'adjectives_adverbs'
        elif type == "Nouns":
            type = 'nouns'
        elif type == "Verbs":
            type = 'verbs'
        direct = 'data/' + type + '.txt'
        self.vocab = Vocab(filename=direct)
        self.vocab.load_words()
        self.vocab.words_dict()
        if not self.vocab.word_dict:
            print(f"Vocabulary file '{direct}' is empty or missing.")
            self._Questions = {}
            return

        # Validate difficulty
        if difficulty not in {1, 2, 3}:
            self._Questions = {}
            return
        available_keys = set()
        if difficulty == 1:
            available_keys = set(word for word in self.vocab.word_dict.keys() if len(word) >= difficulty + 2)
        if difficulty >= 2:
            available_keys = set(word for word in self.vocab.word_dict.keys() if len(word) >= difficulty + 3)
        sample_keys = random.sample(list(available_keys), len1)
        sample_dict = {key: self.vocab.word_dict[key] for key in sample_keys}

        # Generate questions
        self.q = FillInTheBlank(sample_dict)
        self._difficuty = difficulty
        for i in range(len(sample_dict)):
            self.q.generate_question(self._difficuty)
            self.q.add_question()
            # print(q.question_set)
            i+=1
        # if type == '1000words':
        #     type = 'mix'
        # elif type == 'nouns':
        #     type = 'nouns'
        # elif type == 'verbs':
        #     type = 'verbs'
        # elif type == "adjectives_adverbs":
        #     type = "adjectives_adverbs"
        # else:
        #     return
        self._type = type
        self._Questions = self.q.question_set # items contain the question , hint , level and answer

    

    @property
    def word_type(self):
        return self._type
    
    @property
    def questions(self):
        '''
        items()'s key contain the question , hint , level; value is the answer
        '''
        return self._Questions
    
# print(q.question_set)
# View questions and answers
# if __name__ == "__main__":
#     for i in [1,2,3]:
#         print(f"difficulty{i}")
#         question_set = Question_set(type='Mix', len1=100, difficulty=i)
        
#         # 获取生成的问题
#         questions = question_set.questions
        
#         print(len(questions))
        