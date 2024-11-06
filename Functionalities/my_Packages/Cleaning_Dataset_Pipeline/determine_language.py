import os
import pandas as pd
import re
import shutil
from langdetect import detect, LangDetectException

class LanguageDetector:
    def __init__(self, output_file: str, obfuscation_keys: str, description_col: str = 'Description'):
        """
        Initialize the LanguageDetector with a DataFrame and the column containing descriptions.
        
        :param description_col: The column name in the DataFrame to analyze (default: 'Description')
        """
        self.description_col = description_col
        self.output_file = output_file
        self.obfuscation_keys = obfuscation_keys
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of a given text. Handles empty or erroneous inputs.
        
        :param text: The input text for language detection
        :return: The language code ('en' for English, 'nl' for Dutch, 'unknown' if detection fails)
        """
        try:
            # Detect the language of the text
            lang = detect(text)
            if lang == 'en':
                return 'English'
            elif lang == 'nl':
                return 'Dutch'
            else:
                return 'Other'
        except LangDetectException:
            # Return 'Unknown' if detection fails
            return 'Unknown'
        except TypeError:
            # Return 'Unknown' if text is not a string (e.g., NaN)
            return 'Unknown'

    def add_language_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a new column 'Language' to the DataFrame indicating the detected language of each description.
        
        :return: Updated DataFrame with the 'Language' column
        """
        # Apply language detection to each row in the 'Description' column
        df['Language'] = df[self.description_col].apply(self.detect_language)
        return df

    def finish_pipeline(self, df: pd.DataFrame):       
        updated_df = self.add_language_column(df)
        
        # Save the updated DataFrame as a CSV file
        updated_df.to_csv(self.output_file, index=False, encoding='utf-8-sig')

        # Change 'AddressId' column value to 'Company' if the column exists
        if 'AddressId' in df.columns:
            df['Company'] = df.pop('AddressId')

        try:
            # Save the modified dataset
            updated_df.to_csv(self.output_file, index=False, encoding='utf-8-sig')
            print(f"Final cleaned data has been saved to {self.output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")

        output_dir = os.path.dirname(self.output_file)

        shutil.copy(self.obfuscation_keys, output_dir)
        print(f"Obfuscation keys file has been copied")

