# Identity recognition
Api that receives the output of an OCR, and return a dictionnary that contains the name and surname of the patient.  

## Tech
API that uses fastAPI and Pydantic

## Installation

Prérequis:
- Python 3.8
- Conda 

1. Clone the repository on you local machine :

```sh
Copy code
git clone 
cd votre-repo-name
```
2. Create a new env with condat based on environment.yml:

```sh
conda env create -f environment.yml
conda activate lifen_test_env
```

3. Run the API

```sh
uvicorn app:app
```

4. Use the API at  http://localhost:8000/docs.

## Algorithm

The algorithm processes the OCR output with the following logic:

1- Reconstruct the text of the document.
2- Use a rule-based model to extract name information.

The rule is based on the use of capital letters. It identifies a name as a word entirely written in capital letters (like "John MAYER"). Then, it assumes the preceding word is the surname. To avoid mistakenly identifying names of doctors or similar titles, a blacklist of words is implemented (such as "Dr", "Docteur"). If a tuple of two words (word_1, word_2) is identified as being potential surname and name, it will not be returned if word_1 is preceded by a blacklisted word in the text. For example, "Dr Yann LECUN" in the text would prevent ("Yann", "LECUN") from being returned.

#### Potential Improvements:
 - __Handling Mixed Case Names:__ In cases where a name is not entirely written in capital letters, one approach could be to select a tuple of consecutive words (word_1, word_2) where both start with a capital letter. This method would still require the use of a blacklist to avoid confusion with titles.
 - __Database for Surnames:__ Utilize a database to identify surnames, then take the following word (if it starts with a capital letter) or the previous one otherwise to identify the name.
 - __Text Reconstruction with Symbols:__ Consider symbols like "-" in text reconstruction. In the current version, if the OCR identifies three BBoxes for "Jean-Charles" (one for "Jean", one for "-", and one for "Charles"), the reconstructed text from the OCR output will be "Jean - Charles".

