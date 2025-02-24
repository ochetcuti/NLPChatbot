import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#import nltk
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('stopwords')
#nltk.download('punkt_tab')

class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

    def preprocess(self, text):
        if not text:
            return ""
        
        text = text.lower()

        # non-alphabetic characters (keep spaces)
        text = re.sub(r"[^a-z\s]", "", text)

        words = word_tokenize(text)

        # Lemmatize and remove stopwords (little sematic value)
        processed_words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]

        final = " ".join(processed_words)

        print(f'Final Message preprocessing {final}')

        return final
