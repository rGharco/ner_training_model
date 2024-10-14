# ner_training_model
A Named Entity Recognition model that specializes in identifying products from web pages

The model is not finished, as this code only creates the dataset in a json format using the BIO labeling.
You can train the model to your liking using spacy, transformers or any other library.

# ENVIROMENT VARIABELS

WEBSITES_FILE_NAMES = should reference a file , usually in .csv format that has 1 website per line
EXLUCDE_WORDS = this is a list of words that I found during my test datasets, run the code a few times on a list of websites and notice what words it picks up that are not related to the product since the code is meant to pick up classes or ids that have the word product in them , it will sometimes pick things like "add to cart" or "available now" and you can specify them in this variable to ignore them during the labeling process, thus saving some time. It isn't the most efficient way but thats one way I thought about doing it.
