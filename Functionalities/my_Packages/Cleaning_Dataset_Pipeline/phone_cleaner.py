import pandas as pd
import re
from typing import Optional, List

DEFAULT_PHONE_PATTERNS = [
    r'\+?\s?31[\s\d()]*',  # Matches +31 or + 31 followed by digits, spaces, and parentheses
    r'\b[\d\s().-]{8,}\b'  # Matches any sequence of 8 or more digits, spaces, parentheses, dashes, or dots
]

class PhoneNumberCleaner:
    
    def __init__(self, patterns: Optional[List[str]] = None):
        """Initialize the cleaner with custom or default patterns."""
        self.patterns = patterns or DEFAULT_PHONE_PATTERNS

    def mask_phone_numbers(self, description: Optional[str]) -> str:
        """Replace Dutch phone numbers in the description with '***'."""
        if not description:
            return ''
        
        combined_pattern = '|'.join(self.patterns)
        return re.sub(combined_pattern, '***', description)

    def clean_phone_numbers(self, df: pd.DataFrame):
        """Read dataset, mask phone numbers, and save the cleaned dataset."""
        if 'Description' not in df.columns:
            print("The 'Description' column is not found in the DataFrame.")
            return
        
        # Apply the phone number masking function
        df['Description'] = df['Description'].apply(self.mask_phone_numbers)
        
        print("Phone cleaning completed.")
        return df
