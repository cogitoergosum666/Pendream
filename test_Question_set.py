import pytest
import os
from Question_set import Question_set

# #-----------------------------------------------------------
def test_initialization_with_1000words():
    # Test initialization with '1000words' type
    type = "mix"
    question_set = Question_set(type=type, len1=4, difficulty=1)
    assert question_set.word_type == "1000words"
    question_set = Question_set(type='Adjectives/Adverbs', len1=4, difficulty=1)
    assert question_set.word_type == "adjectives_adverbs"
    question_set = Question_set(type='Nouns', len1=4, difficulty=1)
    assert question_set.word_type == "nouns"
    question_set = Question_set(type='Verbs', len1=4, difficulty=1)
    assert question_set.word_type == "verbs"

def test_invalid_type():
    # Test initialization with an invalid type
    invalid_type = "invalid_type"
    question_set = Question_set(type=invalid_type, len1=3, difficulty=2)
    assert len(question_set.questions) == 0, "Invalid type should result in an empty question set."

def test_empty_vocab_file():
    # Test behavior with an empty vocabulary file
    vocab_file = "data/empty.txt"
    with open(vocab_file, "w") as f:
        pass 
    try:
        question_set = Question_set(type="empty", len1=2, difficulty=1)
        assert len(question_set.questions) == 0
    finally:
        if os.path.exists(vocab_file):
            os.remove(vocab_file)

# def test_len1_exceeds_vocab_size():
#     # Test len1 exceeding the number of words in the vocab file
#     with pytest.raises(ValueError):
#         Question_set(type="sample", len1=10, difficulty=2)

def test_questions_property():
    # Test questions property
    question_set = Question_set(type="nouns", len1=3, difficulty=2)
    questions = question_set.questions
    assert isinstance(questions, dict), "Questions should be stored as a dictionary."
    for key, value in questions.items():
        question, hint, level = key
        assert isinstance(question, str), "Question text should be a string."
        assert isinstance(hint, str), "Hint should be a string."
        assert isinstance(level, int), "Difficulty level should be an integer."
        assert isinstance(value, str), "Answer should be a string."

def test_difficulty_level():
    # Test with different difficulty levels
    for difficulty in [1, 2, 3]:
        question_set = Question_set(type="Mix", len1=3, difficulty=difficulty)
        for key, _ in question_set.questions.items():
            _, _, level = key
            assert level == difficulty, f"Expected difficulty level {difficulty}, got {level}."

def test_invalid_difficulty():
    # Test with different difficulty levels
    for difficulty in [0,4]:
        question_set = Question_set(type="nouns", len1=3, difficulty=difficulty)
        assert len(question_set.questions) == 0, f"Invalid difficulty {difficulty} should result in an empty question set."

def test_edge_case_len1_zero():
    # Test len1 set to 0
    question_set = Question_set(type="nouns", len1=0, difficulty=2)
    assert len(question_set.questions) == 0, "No questions should be generated when len1 is 0."

def test_edge_case_nonexistent_difficulty():
    # Test with a difficulty level not in {1, 2, 3}
    question_set = Question_set(type="nouns", len1=3, difficulty=4)
    assert len(question_set.questions) == 0, "No questions should be generated for invalid difficulty levels."

