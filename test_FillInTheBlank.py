import pytest
from FillInTheBlank import FillInTheBlank
from Vocab import Vocab

@pytest.fixture
def vocab_library():
    # Load vocabulary from Vocab class
    vocab = Vocab()
    vocab.load_words()
    vocab.words_dict()
    return vocab.word_dict

def test_generate_question_valid():
    new_vocab = {"test": {"meanings": [["noun", "A procedure intended to establish the quality of something"]]} }
    fill_in_the_blank = FillInTheBlank(new_vocab)
    fill_in_the_blank.generate_question(difficulty=1)
    assert fill_in_the_blank.question is not None, "Question should be generated."
    assert fill_in_the_blank.answer is not None, "Answer should be generated."

def test_generate_question_with_empty_vocab():
    fill_in_the_blank = FillInTheBlank({})
    with pytest.raises(ValueError, match="Vocabulary library is empty. Please set vocab_library before generating questions."):
        fill_in_the_blank.generate_question(difficulty=1)

def test_generate_question_skip_short_words():
    vocab = {
        "a": {"meanings": [["letter", "The first letter of the alphabet"]]},
        "ok": {"meanings": [["adjective", "Used to express agreement or acceptance"]]},
    }
    fill_in_the_blank = FillInTheBlank(vocab)
    fill_in_the_blank.generate_question(difficulty=1)
    question = fill_in_the_blank.question_set
    assert len(question) == 0, "Generated question should not be based on too-short words."

def test_generate_question_difficulty():
    vocab = {
        "planet": {"meanings": [["noun", "A celestial body orbiting a star"]] },
        "galaxy": {"meanings": [["noun", "A system of millions or billions of stars"]] },
        "nebulae": {"meanings": [["noun", "A cloud of gas and dust in outer space"]] },
        "asteroid": {"meanings": [["noun", "A small rocky body orbiting the sun"]] },
        "cometary": {"meanings": [["adjective", "Relating to or resembling a comet"]] },
        "quasars": {"meanings": [["noun", "A massive and extremely remote celestial object"]] },
        "orbits": {"meanings": [["verb", "Moves in a circular path around a star"]] },
        "pulsars": {"meanings": [["noun", "A highly magnetized rotating neutron star"]] },
        "supernova": {"meanings": [["noun", "A star that suddenly increases greatly in brightness"]] },
        "cosmos": {"meanings": [["noun", "The universe seen as a well-ordered whole"]] }
    }
    for i in [1,2,3]:
        fill_in_the_blank = FillInTheBlank(vocab)
        fill_in_the_blank.generate_question(difficulty=i)
        difficulty = fill_in_the_blank.question[2]
        assert difficulty == i
    
def test_add_question(vocab_library):
    fill_in_the_blank = FillInTheBlank(vocab_library)
    fill_in_the_blank.generate_question(difficulty=1)
    fill_in_the_blank.add_question()
    assert len(fill_in_the_blank.question_set) == 1, "Question should be added to the question set."

def test_add_duplicate_question(vocab_library):
    fill_in_the_blank = FillInTheBlank(vocab_library)
    fill_in_the_blank.generate_question(difficulty=1)
    fill_in_the_blank.add_question()
    initial_len = len(fill_in_the_blank.question_set)
    fill_in_the_blank.add_question()  # Attempt to add the same question
    assert len(fill_in_the_blank.question_set) == initial_len, "Duplicate question should not be added."

def test_vocab_library_getter_and_setter(vocab_library):
    fill_in_the_blank = FillInTheBlank(vocab_library)
    assert isinstance(fill_in_the_blank.vocab_library, dict), "vocab_library should be a dictionary."
    new_vocab = {"test": {"meanings": [["noun", "A procedure intended to establish the quality of something"]]} }
    fill_in_the_blank.vocab_library = new_vocab
    assert fill_in_the_blank.vocab_library == new_vocab, "vocab_library setter should update the value."
