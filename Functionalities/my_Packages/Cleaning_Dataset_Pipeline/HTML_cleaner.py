import pandas as pd
from bs4 import BeautifulSoup
from typing import Optional, List
import html
import re

DEFAULT_TAGS_TO_REMOVE = [
    'p', 'div', 'span', 'a', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5',
    'em', 'br', 'u', 'ul', 'li', 'img', 'ol', 'table', 'th', 'tr',
    'td', 'sup', 'label', 'tbody', 'thead', 'section', 'sub', 'hr',
    'blockquote', 'fieldset', 'figure', 'h6', 's', 'colgroup', 'col',
    'pre', 'header', 'enter', 'ready', 'ins', 'figure', 'old', 'aside'
]
DEFAULT_SYMBOLS_TO_REMOVE = ['●']

class HTMLTextCleaner:
    def __init__(self, file_path: str, tags_to_remove: Optional[List[str]] = None, symbols_to_remove: Optional[List[str]] = None):
        self.file_path = file_path
        self.tags_to_remove = tags_to_remove or DEFAULT_TAGS_TO_REMOVE
        self.symbols_to_remove = symbols_to_remove or DEFAULT_SYMBOLS_TO_REMOVE
        self.df = self._load_csv()

    def _load_csv(self) -> pd.DataFrame:
        """Load a CSV file into a DataFrame."""
        try:
            return pd.read_csv(self.file_path, encoding='utf-8')
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(f"Error reading file {self.file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def anonymize_emails(text: str) -> str:
        """Anonymize email addresses in the text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        return re.sub(email_pattern, '***', text)

    def remove_tags(self, text: str) -> str:
        """Remove specified HTML tags while preserving their content."""
        soup = BeautifulSoup(text, "html.parser")
        for tag in self.tags_to_remove:
            for element in soup.find_all(tag):
                element.unwrap()
        return str(soup)

    @staticmethod
    def decode_html_entities(text: str) -> str:
        """Decode HTML entities and replace non-breaking spaces with regular spaces."""
        return html.unescape(text).replace('\xa0', ' ')

    def remove_symbols(self, text: str) -> str:
        """Remove specified symbols from the text."""
        for symbol in self.symbols_to_remove:
            text = text.replace(symbol, '')
        return text

    @staticmethod
    def handle_missing_values(text: str) -> str:
        """Handle missing values in the text."""
        return '' if pd.isna(text) else text

    def clean_description_column(self) -> pd.DataFrame:
        """Clean the 'Description' column by applying all transformation steps."""
        if 'Description' not in self.df.columns:
            raise ValueError("The 'Description' column is not found in the DataFrame.")

        # Apply each transformation step to the 'Description' column
        self.df['Description'] = (
            self.df['Description']
            .apply(self.remove_symbols)
            .apply(self.decode_html_entities)
            .apply(self.remove_tags)
            .apply(self.anonymize_emails)
        )

        print("Data with removed HTML tags has been processed.")
        return self.df