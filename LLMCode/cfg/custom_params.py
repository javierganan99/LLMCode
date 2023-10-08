from pathlib import Path
import os

exclude = []  # Files to exclude
elements2doc = None
# Elements to document (list). If not None, only the functions/classes mathing the name will be documented
languages = ["python"]  # Languages in which the scripts to be documented are written
completion_timeout = 30  # Maximun time to wait for the model to give a response (s)
rewrite = True  # To write the code over the same input path, else it will create
# another path with the same name but adding "surname" to the folder or file
surname = "_analysed"
overwrite = False  # Wheter to overwrite or not the current docstrings
document_prompts = {  # Queries for the model to document function and classes
    "python": {
        "function": Path(__file__).parent
        / f"..{os.path.sep}prompts{os.path.sep}python{os.path.sep}documentFunction.txt",
        "class": Path(__file__).parent
        / f"..{os.path.sep}prompts{os.path.sep}python{os.path.sep}documentClass.txt",
    }
}
query_completion_key = "!<QUERY COMPLETION>!"  # To substitute in the prompt for an element. Prompts must include it
