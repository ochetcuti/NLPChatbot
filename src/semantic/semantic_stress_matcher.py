"""
semantic_stress_matcher.py: handles the sentence embeddings using transformer models for a user session
"""

import pandas as pd
import numpy as np
import os
import pickle
from sklearn.metrics.pairwise import cosine_similarity
#https://github.com/UKPLab/sentence-transformers
from sentence_transformers import SentenceTransformer

class SemanticStressMatcher:
    """
    Uses text embeddings to predict the closest stressor score.
    from preprocessed user input.
    """
    def __init__(self, data_path="SAD_v1.xlsx", model_name="all-MiniLM-L6-v2", cache_path="embedding_cache.pkl", sentences = None, severities = None, labels = None):
        """
        Load pre existing model or generate the embeddings, eval check for final evaluation skip

        Args:
            data_path (str): file name and relative path to dataset
            model_name (str): name of existing installed model
            cache_path (str): file name and relative of pickle file
            sentences (array): array of sentence provided during eval to specificialy train the model (test train eval set)
            severities (array): array of severities provided during eval to specificialy train the model (test train eval set)
            labels (array): array of labels provided during eval to specificialy train the model (test train eval set)
        """
        print('INNIT LOADED')
        self.isEval = False
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.result = {}
        self.embeddings = []
        self.isLoading = False
        if sentences and severities and labels:
            self.sentences = sentences
            self.severity = severities
            self.labels = labels
            self.isEval = True
        if os.path.exists(cache_path):
            print("Loading cached embeddings")
            self.isLoading = True
            try:
                with open(cache_path, "rb") as f:
                    cache = pickle.load(f)
                    self.sentences = cache["sentences"]
                    self.embeddings = cache["embeddings"]
                    self.labels = cache["labels"]
                    self.severity = cache["severity"]
            finally:
                self.isLoading = False
            
        elif os.path.exists(data_path):
            print("Generating embeddings...")
            self.isLoading = True
            try:
                df = pd.read_excel(data_path)
                self.sentences = df['sentence'].tolist()
                self.labels = df['is_stressor'].astype(int).tolist()
                self.severity = df['avg_severity_normalised'].astype(float).tolist()
                self.embeddings = self.model.encode(self.sentences, convert_to_tensor=False)
                with open(cache_path, "wb") as f:
                    pickle.dump({
                        "sentences": self.sentences,
                        "embeddings": self.embeddings,
                        "labels": self.labels,
                        "severity": self.severity
                    }, f)
            finally:
                self.isLoading = False
                print("Embeddings cached.")
        elif self.isEval:
            self.embeddings = self.model.encode(self.sentences, convert_to_tensor=False)
        else:
            raise FileNotFoundError("No valid dataset or cache found, and not in evaluation mode.")

    # find the closes vector to the user input (gets closest)
    def find_closest(self, user_input, top_k=1):
        """
        Find the closest semantic embeddings given a string

        Args:
            user_input (str): pre processed user input to be compared
            top_k (int): selection of the closest embeddings (not implemented)
        Returns:
            array: the closest semantic embeddings with stressor score and similiary
        """
        #input sentence into a high-dimensional vector using the transformer (return as numpy array not PyTorch)
        input_embedding = self.model.encode([user_input], convert_to_tensor=False)
        #closest vectors but as one value (cosine) https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
        similarities = cosine_similarity(input_embedding, self.embeddings)[0]
        
        print(f"DEBUG: SIMILARITIES {similarities}")
        # Get the largest value (most similar)
        best_index = 0
        best_score = similarities[0]
        for i in range(1, len(similarities)):
            if similarities[i] > best_score:
                best_score = similarities[i]
                best_index = i

        self.result ={
            "match": self.sentences[best_index],
            "similarity": float(similarities[best_index]),
            "is_stressor": int(self.labels[best_index]),
            "severity": float(self.severity[best_index])
        }
        print(self.result)
        return self.result


    def threshold_serverity(self):
        """
        thresholds the serverity of the stressor score, based on quantiles

        Returns:
            str: stressor score to be sent to frontend
        """
        # higher is less stressed
        serverity = self.result['severity']
        
        # non stress as low stress
        if not self.result['is_stressor']:
            return "low_stress"

        if(serverity <= 0.020):
            return "high_stress"
        elif (serverity <= 0.306):
            return "moderate_stress"
        else:
            return "low_stress"