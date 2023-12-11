import logging
from typing import List, Union

class RuleBasedModel: 
    """
    A rule-based model to predict first and last names from text.
    """
    black_list = {"Dr", "Dr.", "Docteur"} 
    
    def predict(self, words: Union[List[str], str]) -> dict:
        """Predicts the first and last name from the given text."""

        output = {"prenom": "", "nom": ""}

        if type(words) == str: 
            words = words.split(" ")
        
        if not words:
            logging.warning("Empty text for prediction")
            return output
        
        for i in range(len(words) - 1):
            current, next = words[i], words[i+1]
            if next == next.upper():

                if i>1 and words[i-1] in RuleBasedModel.black_list: 
                    continue
                
                output.update({
                    "prenom": current, 
                    "nom": next
                })
                return output
            
        logging.info("No names were predicted from the text.")
        return output
