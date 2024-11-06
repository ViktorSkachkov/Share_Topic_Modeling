import pandas as pd
import json

class JobPostCleaner:
    def __init__(self, hash_map_path):
        """
        Initializes the JobPostCleaner with a path to a hash map (JSON file).
        :param hash_map_path: Path to the JSON file containing hash values to be removed.
        """
        self.hashes_to_remove = self._load_hashes(hash_map_path)
    
    def _load_hashes(self, hash_map_path):
        """
        Loads the JSON file and extracts the hash values to be removed.
        :param hash_map_path: Path to the JSON file.
        :return: A set of hash values to be removed.
        """
        with open(hash_map_path, 'r') as f:
            hash_map = json.load(f)
        return set(hash_map.values())

    def _remove_hashes(self, text):
        """
        Removes the hashes from a given text, ensuring that words remain separated.
        :param text: The text from which the hash values are to be removed.
        :return: Cleaned text with hashes removed.
        """
        if pd.isnull(text):  # Handle missing data
            return text
        for hash_value in self.hashes_to_remove:
            # Add a space before and after removing the hash to avoid merging words
            text = text.replace(hash_value, ' ')
        # Replace multiple spaces with a single space
        return ' '.join(text.split())

    def clean_columns(self, df, columns):
        """
        Cleans the specified columns of the dataset by removing the hashes.
        :param df: The DataFrame to clean.
        :param columns: List of column names to clean.
        :return: The cleaned DataFrame.
        """
        for column in columns:
            if column in df.columns:
                df[column] = df[column].apply(self._remove_hashes)
        return df

    def initiate_job_post_cleaner(self, df):
        """
        Cleans the specified columns of the DataFrame by removing hashes.
        This method serves as a pipeline entry point.
        :param df: The DataFrame to be cleaned.
        :return: Cleaned DataFrame with hashes removed.
        """
        # Clean the 'Description' column in this example
        cleaned_df = self.clean_columns(df, ['Description'])

        print("Removal of obfuscated items completed.")

        return cleaned_df
