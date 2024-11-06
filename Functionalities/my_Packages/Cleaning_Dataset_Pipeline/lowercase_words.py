import pandas as pd

class LowercaseTransformer:
    def __init__(self):
        """
        Initialize the processor with a pandas DataFrame.
        """
        self.columns = ["Title", "Description"]

    def _convert_to_lowercase(self, text: str) -> str:
        """
        Convert the entire string to lowercase if the text is a string.
        Non-string values remain unchanged.
        """
        if isinstance(text, str):
            return text.lower()  # Convert the whole string to lowercase
        return text

    def lowercase_method(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert all letters to lowercase in the specified columns of the dataframe.
        
        Returns:
        - pd.DataFrame: The updated dataframe with modified columns.
        """
        for column in self.columns:
            if column in df.columns:
                # Apply the lowercase function to each row in the specified column
                df[column] = df[column].apply(self._convert_to_lowercase)
        return df