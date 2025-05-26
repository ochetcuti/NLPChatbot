"""
preprocessor.py: generic text preprocessing module. Used in production
"""

import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextPreprocessor:
    def __init__(self, preprocess_type):
        """
        Creates preprocessing object

        Args:
            preprocess_type (int): Preprocessing setting 
            1 = full preprocessing
            2 = minimal preprocessing
        """
        self.lemmatizer = WordNetLemmatizer()
        self.preprocess_type = preprocess_type
        self.stop_words = set(stopwords.words("english"))

    def preprocess(self, text):
        """
        Preprcesses text

        Args:
            text (str): preprocessing string
        
        Returns:
            str: preprocesed text string to be passed to model
            
        """
        # Full preprocessing
        if self.preprocess_type == 1:
            if not text:
                return ""
            print(f"DEBUG: TextPreprocessor Pre\n{text}\n")
            # Remove all non space breaks and replace with " " (/n /r etc), strip spaces from start and end
            text = re.sub(r"\s+", " ", text.strip())

            # Remove captial letter at the start of the sentence
            if re.match(r'^[A-Z]', text):
                text = text[0].lower() + text[1:]

            #tokenisation
            words = word_tokenize(text)
            print(words)

            # lemmantizeation
            processed_words = []
            for word in words:
                # Check for stopwords
                if word.lower() in self.stop_words:
                    continue 
                # Lemmatize
                lemmatized = self.lemmatizer.lemmatize(word)
                processed_words.append(lemmatized)

            print(processed_words)

            # Return back to a sentence
            final = " ".join(processed_words)

            print(f'DEBUG: TextPreprocessor Final\n{final}\n')

            return final
        #embeddings preprocessing
        elif self.preprocess_type  == 2:
            if not text:
                return ""
            print(f"DEBUG: TextPreprocessor Pre\n{text}\n")
            # Remove all non space breaks and replace with " " (/n /r etc), strip spaces from start and end
            remove_breakes = re.sub(r"\s+", " ", text.strip())
            print(f'DEBUG: TextPreprocessor Final\n{remove_breakes}\n')
            return remove_breakes
