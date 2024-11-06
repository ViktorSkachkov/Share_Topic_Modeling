import pandas as pd
import re
import json
from typing import Dict

class ObfuscationCleaner:
    """A class to handle the obfuscation and cleaning of dataset columns."""

    def __init__(self, replacements_file: str):
        """Initialize the ObfuscationCleaner with a replacements file."""
        self.replacements = self._load_replacements(replacements_file)

    @staticmethod
    def _load_replacements(file_path: str) -> Dict[str, str]:
        """Load replacement rules from a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def _replace_urls(text: str) -> str:
        """Replace URLs containing 'www.' or '.com' with '***'."""
        url_pattern = r'\b(?:www\.\S*|[^ ]*\.com)\b'
        return re.sub(url_pattern, '***', text)

    def _replace_parts_of_words(self, text: str) -> str:
        """Replace parts of words based on the replacement dictionary."""
        pattern = '|'.join(re.escape(key) for key in self.replacements)
        return re.sub(pattern, lambda match: self.replacements[match.group()], text)

    @staticmethod
    def _insert_space_after_punctuation(text: str) -> str:
        """Ensure there's a space after punctuation marks."""
        return re.sub(r"([,!?;])(\S)", r"\1 \2", text)

    def _process_column(self, df: pd.DataFrame, column: str):
        """Apply all transformations to a specific column in the DataFrame."""
        if column in df.columns:
            df[column] = df[column].apply(self._replace_urls) \
                                    .apply(self._replace_parts_of_words) \
                                    .apply(self._insert_space_after_punctuation)

    def obfuscate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply obfuscation to the 'Description' and 'Title' columns in the dataset."""
        for column in ["Description", "Title"]:
            self._process_column(df, column)
        
        print("Obfuscated data has been processed.")
        return df
