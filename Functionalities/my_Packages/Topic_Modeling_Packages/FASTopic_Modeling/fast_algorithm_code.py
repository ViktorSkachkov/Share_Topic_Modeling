import pandas as pd
import os
import pickle
import re
from fastopic import FASTopic
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
from nltk import ngrams
import nltk

nltk.download('punkt')

class TopicModelingPipeline:
    def __init__(self, file_path: str, model_file: str, output_file: str, 
                 custom_stopwords_file: str, english_stopwords_file: str, 
                 dutch_stopwords_file: str, output_subfolder: str, num_topics: int, 
                 num_top_words: int, epochs: int):
        self.file_path = file_path
        self.model_file = model_file
        self.output_file = output_file
        self.custom_stopwords_file = custom_stopwords_file
        self.english_stopwords_file = english_stopwords_file
        self.dutch_stopwords_file = dutch_stopwords_file
        self.num_topics = num_topics
        self.num_top_words = num_top_words
        self.epochs = epochs
        self.stopwords = self.load_stopwords()
        self.model = None

    def load_dataset_from_csv(self) -> list:
        df = pd.read_csv(self.file_path)
        dataset = df['Description'].dropna().tolist()
        return dataset

    def load_stopwords(self) -> set:
        stopwords = set()

        # List of stopword files to be loaded
        stopword_files = [
            self.custom_stopwords_file,
            self.english_stopwords_file,
            self.dutch_stopwords_file
        ]

        for file_path in stopword_files:
            # Normalize the file path to an absolute path
            absolute_path = os.path.abspath(file_path)

            # Check if the file exists
            if not os.path.isfile(absolute_path):
                print(f"Warning: Stopword file not found: {absolute_path}")
                continue  # Skip this file if it does not exist
            
            with open(absolute_path, 'r', encoding='utf-8') as f:
                stopwords.update(f.read().splitlines())
        return stopwords

    def preprocess_text(self, text: str, n: int = 2) -> list:
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokens = [word for word in text.split() if word not in self.stopwords]
        
        # Generate n-grams
        n_grams = [' '.join(ng) for ng in ngrams(tokens, n)]  # Create bigrams
        return tokens + n_grams  # Return both tokens and n-grams

    def apply_fastopic(self, dataset: list):
        self.model = FASTopic(num_topics=self.num_topics, num_top_words=self.num_top_words, epochs=self.epochs, verbose=False)
        self.model.fit(dataset)

        # Create a Gensim Dictionary from the dataset
        self.dictionary = Dictionary([text.split() for text in dataset])

    def calculate_umass_coherence(self, processed_dataset):
        # Prepare the texts in a format suitable for coherence calculation
        # Note: filtered_dataset contains the processed text from run method
        texts = [text.split() for text in processed_dataset]  # Split the processed text back into tokens
    
        # Create a Gensim Dictionary from the texts
        self.dictionary = Dictionary(texts)

        # Use the FASTopic model to retrieve topics
        topics = []
        for i in range(self.num_topics):
            topic_words_with_weights = self.model.get_topic(topic_idx=i, num_top_words=self.num_top_words)
            topic_words = [word for word, weight in topic_words_with_weights]  # Extract only the words
            topics.append(topic_words)  # Append the list of words for each topic
    
        # Prepare the coherence model
        coherence_model = CoherenceModel(topics=topics, texts=texts, dictionary=self.dictionary, coherence='u_mass')
    
        # Get the coherence score
        coherence_score = coherence_model.get_coherence()
        print(f"UMass Coherence Score: {coherence_score}")
        return coherence_score

    def save_model(self):
        with open(self.model_file, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self):
        with open(self.model_file, 'rb') as f:
            self.model = pickle.load(f)

    def save_topics_to_file(self, num_topics: int, num_top_words: int):
        with open(self.output_file, 'w') as f:
            for i in range(num_topics):
                topic_words_with_weights = self.model.get_topic(topic_idx=i, num_top_words=num_top_words)
                topic_words = [word for word, weight in topic_words_with_weights]
                f.write(f"Topic {i + 1}: {', '.join(topic_words)}\n")

    def display_topics(self, num_topics: int, num_top_words: int):
        print("Topics identified by FASTopic:")
        print(f"Type of num_topics: {type(self.num_topics)}")  # Debugging line
        for i in range(num_topics):
            topic_words_with_weights = self.model.get_topic(topic_idx=i, num_top_words=num_top_words)
            topic_words = [word for word, weight in topic_words_with_weights]
            print(f"Topic {i + 1}: {', '.join(topic_words)}")

    def run(self):
        # Check if model exists, if not, train and save it
        if os.path.exists(self.model_file):
            print("Loading existing model...")
            self.load_model()
        else:
            print("Training new model...")
            dataset = self.load_dataset_from_csv()
            
            # Preprocess the dataset to include n-grams
            self.processed_dataset = []
            for text in dataset:
                processed_text = self.preprocess_text(text, n=2)  # Change n=2 for bigrams, or n=3 for trigrams
                self.processed_dataset.append(' '.join(processed_text))  # Join tokens back into a single string
    
            self.apply_fastopic(self.processed_dataset)
            self.save_model()
    
        # Display and save topics
        self.display_topics(self.num_topics, self.num_top_words)
        self.save_topics_to_file(self.num_topics, self.num_top_words)

        self.calculate_umass_coherence(self.processed_dataset)
        
        print(f"Topics saved to {self.output_file}")