import pandas as pd
import re

class PunctuationHandler:
    def __init__(self):
        """
        Initialize the cleaner with the target columns.
        """
        self.columns = ["Title", "Description"]

    def _clean_text(self, text: str) -> str:
        """
        Cleans the text by:
        1. Removing ".", ",", "!", "-", and "?".
        2. Replacing "+" with "p".
        3. Replacing "/" with a space.
        4. Replacing "#" with "sharp".
        
        Non-string values remain unchanged.
        """
        if isinstance(text, str):
            # Step 1: Remove ".", ",", "!", "-", "?"
            cleaned_text = re.sub(r'[.,!?-]', '', text)
            
            # Step 2: Replace "++" with "pp" unless it touches an interval on the left side
            cleaned_text = re.sub(r'(?<! )\+\+', 'pppp', cleaned_text)
            
            # Step 3: Replace "/" with space
            cleaned_text = cleaned_text.replace('/', ' ')
            
            # Step 4: Replace "#" with "sharp" unless it touches an interval on the left side
            cleaned_text = re.sub(r'(?<! )#', 'sharp', cleaned_text)
            
            return cleaned_text
        return text

    def initiate_punctuation_handling(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies text cleaning to the 'Title' and 'Description' columns of the DataFrame.
        
        Returns:
        - pd.DataFrame: The cleaned dataframe with updated columns.
        """
        for column in self.columns:
            if column in df.columns:
                df[column] = df[column].apply(self._clean_text)
        return df