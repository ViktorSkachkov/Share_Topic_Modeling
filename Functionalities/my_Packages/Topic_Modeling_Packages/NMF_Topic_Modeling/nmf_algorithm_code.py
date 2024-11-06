import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.decomposition import NMF
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import numpy as np

# Ensure NLTK stopwords are downloaded
nltk.download('punkt')
nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self, stopword_files):
        self.stopwords = self.load_stopwords(stopword_files)
        
    def load_stopwords(self, stopword_files):
        stopwords_set = set(stopwords.words('english'))
        for file in stopword_files:
            with open(file, 'r', encoding='utf-8') as f:
                file_stopwords = f.read().splitlines()
                stopwords_set.update(file_stopwords)
        return stopwords_set
    
    def preprocess(self, texts):
        processed_texts = []
        for text in texts:
            tokens = word_tokenize(text.lower())
            filtered_tokens = [word for word in tokens if word.isalpha() and word not in self.stopwords]
            processed_texts.append(' '.join(filtered_tokens))
        return processed_texts

class NMFModel:
    def __init__(self, n_topics, data, stopword_files, num_top_words, epochs, output_subfolder):
        self.n_topics = n_topics
        self.data = data
        self.num_top_words = num_top_words
        self.epochs = epochs
        self.output_subfolder = output_subfolder
        self.preprocessor = TextPreprocessor(stopword_files)
        self.vectorizer = TfidfVectorizer()
        self.model = None

        # Ensure the output folder exists
        os.makedirs(self.output_subfolder, exist_ok=True)

    def fit(self):
        processed_texts = self.preprocessor.preprocess(self.data['Description'])
        doc_term_matrix = self.vectorizer.fit_transform(processed_texts)
        # Set max_iter to self.epochs for controlling NMF iterations
        self.model = NMF(n_components=self.n_topics, random_state=42, max_iter=self.epochs)
        self.doc_term_matrix = doc_term_matrix
        self.topic_matrix = self.model.fit_transform(doc_term_matrix)

    def display_topics(self):
        # Save topics to a file
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        for idx, topic in enumerate(self.model.components_):
            topics.append([feature_names[i] for i in topic.argsort()[-self.num_top_words:]])
        
        file_path = os.path.join(self.output_subfolder, 'topics.txt')
        with open(file_path, 'w') as f:
            for i, topic in enumerate(topics, 1):
                f.write(f"Topic {i}:\n")
                f.write(", ".join(topic) + "\n\n")
        
        print(f"Topics saved to {file_path}")
        return topics

    def calculate_topic_coherence(self):
        # Simple coherence metric based on word similarity within topics
        coherence_scores = []
        for topic_idx, topic in enumerate(self.model.components_):
            top_words_idx = topic.argsort()[-self.num_top_words:]
            pairwise_distances = [
                np.linalg.norm(self.model.components_[:, top_words_idx[i]] - self.model.components_[:, top_words_idx[j]])
                for i in range(len(top_words_idx)) for j in range(i + 1, len(top_words_idx))
            ]
            coherence_scores.append(np.mean(pairwise_distances))

        coherence_score = np.mean(coherence_scores)
        return coherence_score

    def calculate_topic_diversity(self):
        topics = self.display_topics()
        unique_words = set(word for topic in topics for word in topic)
        topic_diversity = len(unique_words) / (self.n_topics * self.num_top_words)
        return topic_diversity

    def calculate_silhouette_score(self):
        # Clustering quality evaluation
        kmeans = KMeans(n_clusters=self.n_topics, random_state=42)
        labels = kmeans.fit_predict(self.topic_matrix)
        score = silhouette_score(self.topic_matrix, labels)
        return score

    def evaluate_clustering_stability(self, num_runs=5):
        # Measure clustering stability across multiple runs
        stability_scores = []
        for _ in range(num_runs):
            model = NMF(n_components=self.n_topics, random_state=None, max_iter=self.epochs)
            topic_matrix = model.fit_transform(self.doc_term_matrix)
            kmeans = KMeans(n_clusters=self.n_topics, random_state=42)
            labels = kmeans.fit_predict(topic_matrix)
            score = silhouette_score(topic_matrix, labels)
            stability_scores.append(score)

        avg_stability_score = np.mean(stability_scores)
        return avg_stability_score
    
    def calculate_cosine_similarity(self):
        """Calculate the cosine similarity between topics."""
        # Calculate cosine similarity between topic components
        cosine_sim = cosine_similarity(self.model.components_)
        return cosine_sim