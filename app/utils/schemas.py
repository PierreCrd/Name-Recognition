from pydantic import BaseModel
from typing import List
import logging

class BBox(BaseModel):
    """
    Represents a bounding box with coordinates.
    """
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    
class WordBBox(BaseModel):
    """
    Represents a word and its associated bounding box.
    """
    text: str
    bbox: BBox

    @staticmethod
    def are_aligned(word_bbox_1: 'WordBBox', word_bbox_2: 'WordBBox') -> bool:
        """
        Return True if the WordBBoxes are aligned, False otherwise.
        """
        word_bbox_1_y_mean = (word_bbox_1.bbox.y_min + word_bbox_1.bbox.y_max) / 2

        is_mean_above_min = word_bbox_1_y_mean > word_bbox_2.bbox.y_min
        is_mean_below_max = word_bbox_1_y_mean < word_bbox_2.bbox.y_max
        return is_mean_above_min and is_mean_below_max
    
class Page(BaseModel):
    """
    Represents a page containing multiple WordBBoxes.
    """
    words: List[WordBBox]

class OCRData(BaseModel):
    """
    Represents OCR data containing multiple pages.
    """
    pages: List[Page]

    def _get_word_bboxes(self) -> List[WordBBox]:
        """
        Extracts and returns all WordBBox objects from the OCR data.

        Returns:
            List[WordBBox]: A list of all WordBBox objects in the OCR data.
        """
        word_bboxes = []
        for page in self.pages:
            for word_bbox in page.words:
                word_bboxes.append(word_bbox)

        if not word_bboxes:
            logging.warning("No BBoxes were extracted from OCR data.")
        return word_bboxes
    
    def _get_lines(self, word_bboxes: List[WordBBox]) -> List[List[WordBBox]]:
        """
        Organizes the WordBBoxes into lines of text based on their alignment.

        Returns:
            List[List[WordBBox]]: A list of lines, each line being a list of WordBBox objects.
        """
        if not word_bboxes:
            return []
        
        lines = []
        word_bboxes = sorted(word_bboxes, key=lambda word_bbox: word_bbox.bbox.y_min)
        current_line = [word_bboxes[0]]

        for word_bbox in word_bboxes[1:]: 
            if WordBBox.are_aligned(word_bbox, current_line[-1]):
                current_line.append(word_bbox)
            else: 
                current_line.sort(key=lambda word_bbox: word_bbox.bbox.x_min)
                lines.append(current_line)
                current_line = [word_bbox]
        lines.append(current_line)
        return lines
    
    def get_text(self) -> str:
        """
        Extracts the text from WordBBoxes, organized by line.

        Returns:
            List[str]: A list of strings, each representing a word of the text (sorted by line).
        """
        word_bboxes = self._get_word_bboxes()
        lines = self._get_lines(word_bboxes)

        text = " ".join([word_bbox.text for line in lines for word_bbox in line])
        return text
    