import pandas as pd
import json
import re
from typing import List, Dict, Set

class WordReplacer:
    def __init__(self, replacements_file: str, stopword_files: List[str]):
        """Initializes the WordReplacer with replacement words and stopwords."""
        self.replacements_file = replacements_file
        self.stopword_files = stopword_files

        # Load replacements and stopwords from files
        self.replacements = self.load_replacements(replacements_file)
        self.stopwords = self.load_stopwords(stopword_files)

        self.columns=['Description', 'Title']

    @classmethod
    def from_files(cls, json_file: str, stopword_files: List[str]) -> 'WordReplacer':
        """Factory method to load replacements and stopwords from files."""
        replacements = cls.load_replacements(json_file)
        stopwords = cls.load_stopwords(stopword_files)
        return cls(replacements, stopwords)

    @staticmethod
    def load_replacements(json_file: str) -> Dict[str, str]:
        """Loads the replacement words from a JSON file."""
        with open(json_file, 'r') as f:
            return json.load(f)

    @staticmethod
    def load_stopwords(stopword_files: List[str]) -> Set[str]:
        """Loads stopwords from multiple text files and normalizes them to lowercase."""
        stopwords = set()
        for file in stopword_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:  # Specify encoding
                    stopwords.update(word.strip().lower() for word in f.readlines())
            except UnicodeDecodeError:
                print(f"Error reading {file}, trying a different encoding...")
                with open(file, 'r', encoding='utf-8-sig') as f:  # Try UTF-8 with BOM
                    stopwords.update(word.strip().lower() for word in f.readlines())
        return stopwords


    def should_replace(self, word: str) -> bool:
        """Checks if a word should be replaced, i.e., it's not a stopword."""
        return word.lower() not in self.stopwords
    
    def replace_text(self, text):
        # Iterate through each item in the dictionary
        for key, value in self.replacements.items():
            # Use regex to replace the key with value even if merged with symbols
            # The pattern allows for any non-word character (including symbols) before/after
            text = re.sub(r'(?<!\w)' + re.escape(key) + r'(?!\w)', value, text)
        return text

    def process_dataframe(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Processes a DataFrame and replaces words in the specified columns."""
        for column in columns:
            df[column] = df[column].apply(self.replace_text)
        return df
    
    def initiate_word_replacer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns the processed DataFrame.
        """

        # Process the DataFrame to apply replacements to both 'Description' and 'Title'
        processed_df = self.process_dataframe(df, self.columns)

        print("Replacement of words")
        
        # Return the processed DataFrame
        return processed_df