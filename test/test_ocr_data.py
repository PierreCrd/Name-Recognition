import pytest
from app.utils.schemas import BBox, WordBBox, Page, OCRData
import json

word1 = WordBBox(text="Hello", bbox=BBox(x_min=0, x_max=10, y_min=0, y_max=10))
word2 = WordBBox(text="World", bbox=BBox(x_min=10, x_max=20, y_min=20, y_max=30))

page = Page(words=[word1, word2])

ocr_data = OCRData(pages=[page])

def test_get_word_bboxes():
    word_bboxes = ocr_data._get_word_bboxes()

    assert len(word_bboxes) == 2
    assert word_bboxes[0].text == "Hello"
    assert word_bboxes[1].text == "World"

def test_get_lines():
    word_bboxes = ocr_data._get_word_bboxes()
    lines = ocr_data._get_lines(word_bboxes)

    assert len(lines) == 2
    assert lines[0][0].text == "Hello"
    assert lines[1][0].text == "World"

def test_get_text():
    text = ocr_data.get_text()

    assert text == "Hello World"
