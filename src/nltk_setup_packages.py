import nltk
from nltk.data import find
from nltk import download

def install_nltk_resources():
    resources = [
        'punkt',
        'wordnet',
        'stopwords',
        'punkt_tab',
        'vader_lexicon'
    ]

    for resource in resources:
        try:
            find(resource)
        except LookupError:
            print(f"Downloading NLTK resource: {resource}")
            download(resource)
