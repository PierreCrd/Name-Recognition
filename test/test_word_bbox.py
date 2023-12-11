import pytest
from app.utils.schemas import WordBBox, BBox

bbox1 = BBox(x_min=0, x_max=10, y_min=0, y_max=10)
bbox2 = BBox(x_min=5, x_max=15, y_min=0, y_max=10)
bbox3 = BBox(x_min=10, x_max=20, y_min=10, y_max=20)

word_bbox1 = WordBBox(text="Hello", bbox=bbox1)
word_bbox2 = WordBBox(text="World", bbox=bbox2)
word_bbox3 = WordBBox(text="Test", bbox=bbox3)

def test_are_aligned_true():
    assert WordBBox.are_aligned(word_bbox1, word_bbox2)

def test_are_aligned_false():
    assert not WordBBox.are_aligned(word_bbox1, word_bbox3)
