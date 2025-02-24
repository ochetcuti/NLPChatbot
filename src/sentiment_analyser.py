
from nltk.sentiment import SentimentIntensityAnalyzer
#import nltk
#nltk.download("vader_lexicon")

class SentimentAnalyser:
    def __init__(self):
        """Initialize VADER sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()

    def analyse_sentiment(self, text):
        if not text:
            return "neutral"

        sentiment_score = self.analyzer.polarity_scores(text)

        # stress level based on VADER sentiment score
        if sentiment_score["compound"] <= -0.4:
            return "high_stress"
        elif sentiment_score["compound"] <= 0.2:
            return "moderate_stress"
        else:
            return "low_stress"
