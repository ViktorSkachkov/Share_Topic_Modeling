import nltk
# nltk.download('punkt')  # Download necessary NLTK data (if not already downloaded)
nltk.download('stopwords')
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
import pandas as pd

def detect_english_or_dutch(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    
    for language in ['english', 'dutch']:
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)
        languages_ratios[language] = len(common_elements)
    
    detected_language = max(languages_ratios, key=languages_ratios.get)
    
    return detected_language

#Read Excel file
file_path = 'ActualJobPostings/Alljobs.xlsx'  # Update with your file path
df = pd.read_excel(file_path)

# Apply language detection function to each row in the 'job-description' column
df['detected_language'] = df['job-description'].apply(detect_english_or_dutch)

# Save the DataFrame with the added column to a new Excel file
output_file_path = 'ActualJobPostings/lang.xlsx'  # Update with your desired output file path
df.to_excel(output_file_path, index=False)

print("Language detection completed. Output saved to", output_file_path)

# Example usage
# text = "This is a sample English text"
# detected_language = detect_english_or_dutch(text)
# print("Detected language:", detected_language)

# text = "Dit is een voorbeeld van Nederlandse tekst"
# detected_language = detect_english_or_dutch(text)
# print("Detected language:", detected_language)
