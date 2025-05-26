"""
sentiment_analyser.py: scripted analysis module
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SentimentAnalyser:
    def __init__(self):
        """Initialise VADER sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()

    def analyse_sentiment(self, text):
        """
        uses VADER sentiment to get polarity scores string stress level

        Args:
            text (str): preprocessed string input
        Returns:
            str: stress level
        """
        sentiment_score = self.analyzer.polarity_scores(text)

        # stress level based on VADER sentiment score
        if sentiment_score["compound"] <= -0.5:
            return "high_stress"
        elif sentiment_score["compound"] < 0.5:
            return "moderate_stress"
        else:
            return "low_stress"
