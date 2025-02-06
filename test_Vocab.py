import pytest
import json
import os
from Vocab import Vocab

@pytest.fixture
def setup_vocab_files(tmp_path):
    words_file = tmp_path / "test_words.txt"
    dictionary_file = tmp_path / "test_dictionary.json"

    with open(words_file, "w") as f:
        f.write("apple\nbanana\ncarrot\n12345\norange\n\n") 

    dictionary_data = {
        "APPLE": {"MEANINGS": [["noun", "A fruit that grows on trees"]]},
        "BANANA": {"MEANINGS": [["noun", "A long yellow fruit"]]},
        "CARROT": {"MEANINGS": [["noun", "An orange root vegetable"]]},
    }
    with open(dictionary_file, "w") as f:
        json.dump(dictionary_data, f)

    return words_file, dictionary_file

def test_load_words_success(setup_vocab_files):
    words_file, _ = setup_vocab_files
    vocab = Vocab(filename=words_file)

    vocab.load_words()
    assert vocab.words == ["apple", "banana", "carrot", "orange"]

def test_load_words_file_not_found():
    vocab = Vocab(filename="nonexistent_file.txt")
    vocab.load_words()
    assert vocab.words == []

def test_words_dict_success(setup_vocab_files):
    words_file, dictionary_file = setup_vocab_files
    vocab = Vocab(filename=words_file, dictionary_file=dictionary_file)

    vocab.load_words()
    vocab.words_dict()

    assert "apple" in vocab.word_dict
    assert vocab.word_dict["apple"]["meanings"] == [["noun", "A fruit that grows on trees"]]
    assert "orange" not in vocab.word_dict

def test_words_dict_file_not_found(setup_vocab_files):
    words_file, _ = setup_vocab_files
    vocab = Vocab(filename=words_file, dictionary_file="nonexistent_file.json")

    vocab.load_words()
    vocab.words_dict()
    assert vocab.word_dict == {}

def test_words_dict_invalid_json(tmp_path, setup_vocab_files):

    invalid_json_file = tmp_path / "invalid_dictionary.json"
    invalid_json_file.write_text("{ invalid JSON }") 

    words_file, _ = setup_vocab_files
    vocab = Vocab(filename=words_file, dictionary_file=invalid_json_file)

    vocab.load_words()
    vocab.words_dict()
    assert vocab.word_dict == {}

def test_empty_words_file(tmp_path):

    empty_file = tmp_path / "empty_words.txt"
    empty_file.touch() 

    vocab = Vocab(filename=empty_file)
    vocab.load_words()
    assert vocab.words == []

def test_empty_dictionary_file(tmp_path, setup_vocab_files):
    empty_dict_file = tmp_path / "empty_dictionary.json"
    empty_dict_file.touch() 

    words_file, _ = setup_vocab_files
    vocab = Vocab(filename=words_file, dictionary_file=empty_dict_file)

    vocab.load_words()
    vocab.words_dict()
    assert vocab.word_dict == {}
