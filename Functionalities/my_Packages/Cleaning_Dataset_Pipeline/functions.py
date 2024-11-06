import os
import pandas as pd
from typing import List
from .HTML_cleaner import HTMLTextCleaner
from .obfuscation_cleaner import ObfuscationCleaner
from .phone_cleaner import PhoneNumberCleaner
from .determine_language import LanguageDetector
from .remove_invalid_data import InvalidDataRemover
from .remove_duplicates import JobPostDeduplicator
from .remove_obfuscated_terms import JobPostCleaner
from .lowercase_words import LowercaseTransformer
from .handle_punctuation import PunctuationHandler

def clean_dataset_pipeline(input_file: str, output_file: str, obfuscation_keys: str = None) -> None:
    # Load and clean the dataset in a single pipeline
    
    ''' if obfuscation_keys is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        obfuscation_keys = os.path.join(current_dir, 'keys', 'combined_data_final.json') '''

    HTML_cleaner = HTMLTextCleaner(input_file)
    clean_description_column = HTML_cleaner.clean_description_column

    obfuscator = ObfuscationCleaner(obfuscation_keys)

    phone_cleaner = PhoneNumberCleaner()

    determine_language = LanguageDetector(output_file, obfuscation_keys)

    # Load and clean the dataset in a single pipeline
    df = (
        clean_description_column()
        .pipe(phone_cleaner.clean_phone_numbers)
        .pipe(obfuscator.obfuscate)
        .pipe(determine_language.finish_pipeline)
    )


def clean_dataset_pipeline2(input_file: str, output_file: str, output_subfolder: str, obfuscation_keys: str = None) -> None:
    # Load and clean the dataset in a single pipeline
    
    ''' if obfuscation_keys is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        obfuscation_keys = os.path.join(current_dir, 'keys', 'combined_data_final.json') '''

    HTML_cleaner = HTMLTextCleaner(input_file)
    clean_description_column = HTML_cleaner.clean_description_column

    obfuscator = ObfuscationCleaner(obfuscation_keys)

    phone_cleaner = PhoneNumberCleaner()

    determine_language = LanguageDetector(output_file, obfuscation_keys)

    hash_remover = JobPostCleaner(obfuscation_keys)

    invalid_data_remover = InvalidDataRemover(output_subfolder)

    duplicates_remover = JobPostDeduplicator(output_subfolder)

    # Use a pipeline
    df = (
        clean_description_column()
        .pipe(phone_cleaner.clean_phone_numbers)
        .pipe(obfuscator.obfuscate)
        .pipe(hash_remover.initiate_job_post_cleaner)
        .pipe(duplicates_remover.deduplicate_and_save)
        .pipe(invalid_data_remover.save_cleaned_data)
        .pipe(determine_language.finish_pipeline)
    )


def clean_dataset_pipeline3(input_file: str, output_file: str, output_subfolder: str, stopword_files: List[str], replacements_file: str, obfuscation_keys: str = None) -> None:
    # Load and clean the dataset in a single pipeline
    
    ''' if obfuscation_keys is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        obfuscation_keys = os.path.join(current_dir, 'keys', 'combined_data_final.json') '''

    HTML_cleaner = HTMLTextCleaner(input_file)
    clean_description_column = HTML_cleaner.clean_description_column

    obfuscator = ObfuscationCleaner(obfuscation_keys)

    phone_cleaner = PhoneNumberCleaner()

    determine_language = LanguageDetector(output_file, obfuscation_keys)

    hash_remover = JobPostCleaner(obfuscation_keys)

    invalid_data_remover = InvalidDataRemover(output_subfolder)

    duplicates_remover = JobPostDeduplicator(output_subfolder)

    lowercase_transformer = LowercaseTransformer()

    punctuation_handler = PunctuationHandler()

    # Use a pipeline
    df = (
        clean_description_column()
        .pipe(phone_cleaner.clean_phone_numbers)
        .pipe(obfuscator.obfuscate)
        .pipe(hash_remover.initiate_job_post_cleaner)
        .pipe(duplicates_remover.deduplicate_and_save)
        .pipe(invalid_data_remover.save_cleaned_data)
        .pipe(punctuation_handler.initiate_punctuation_handling)
        .pipe(lowercase_transformer.lowercase_method)
        .pipe(determine_language.finish_pipeline)
    )