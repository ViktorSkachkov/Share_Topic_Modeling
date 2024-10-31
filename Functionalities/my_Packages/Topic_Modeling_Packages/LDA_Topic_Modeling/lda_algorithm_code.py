import pandas as pd
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances, silhouette_score
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Ensure you have downloaded the punkt and stopwords
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


class LDAModel:
    def __init__(self, num_topics: int, data: pd.DataFrame, stopword_files: list, num_top_words: int, epochs: int):
        self.num_topics = num_topics
        self.data = data
        self.preprocessor = TextPreprocessor(stopword_files)
        self.vectorizer = CountVectorizer()
        self.model = None
        self.num_top_words = num_top_words
        self.epochs = epochs

    def fit(self):
        # Preprocess the data and create the document-term matrix
        processed_texts = self.preprocessor.preprocess(self.data['Description'])
        self.doc_term_matrix = self.vectorizer.fit_transform(processed_texts)
        
        # Instantiate and fit the LDA model with verbose logging
        self.model = LatentDirichletAllocation(
            n_components=self.num_topics,
            random_state=42,
            max_iter=self.epochs,
            verbose=1  # Enables progress logging in the terminal
        )
        self.model.fit(self.doc_term_matrix)

    def evaluate(self):
        # Use score() for log-likelihood and perplexity() for perplexity
        coherence_score = self.model.score(self.doc_term_matrix)  # This is the log-likelihood
        perplexity_score = self.model.perplexity(self.doc_term_matrix)
        return coherence_score, perplexity_score

    def topic_diversity(self):
        topics = self.display_topics()
        unique_words = set(word for topic in topics for word in topic)
        return len(unique_words) / (self.num_topics * self.num_top_words)  # Normalized diversity score

    def hierarchy_quality(self):
        topic_word_matrix = self.model.components_
        distances = pairwise_distances(topic_word_matrix)
        return distances

    def clustering(self, n_clusters=5):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(self.doc_term_matrix)
        silhouette_avg = silhouette_score(self.doc_term_matrix, kmeans.labels_)
        return silhouette_avg

    def classification(self, labels):
        if len(labels) != len(self.data):
            raise ValueError("Number of labels must match number of documents.")
        
        X_train, X_test, y_train, y_test = train_test_split(self.doc_term_matrix, labels, test_size=0.2, random_state=42)
        classifier = LogisticRegression(max_iter=1000)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        report = classification_report(y_test, y_pred)
        return report

    def display_topics(self):
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        for idx, topic in enumerate(self.model.components_):
            topics.append([feature_names[i] for i in topic.argsort()[-self.num_top_words:]])
        return topics

    def save_topics(self, output_subfolder):
        # Ensure the output subfolder exists
        os.makedirs(output_subfolder, exist_ok=True)  # Create the directory if it doesn't exist
        
        topics = self.display_topics()
        file_path = os.path.join(output_subfolder, 'topics.txt')  # Save in the specified folder

        with open(file_path, 'w') as f:
            for i, topic in enumerate(topics, 1):
                f.write(f"Topic {i}:\n")
                f.write(", ".join(topic) + "\n\n")
        
        print(f"Topics saved to {file_path}")