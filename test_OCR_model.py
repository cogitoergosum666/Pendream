import pytest
from OCR_model import OCR_model

def test_OCR_model():
    model = OCR_model("data/1.jpg")
    text = model.start_OCR()
    text = text.replace(" ", "")
    assert text == 'ae'