# Importing necessary libraries and modules
from transformers import pipeline  # For loading the pre-trained NER (Named Entity Recognition) models
import pandas as pd  # For data manipulation and file operations
import wordninja  # For splitting concatenated words (although it's not used in this particular script)
from langdetect import detect, LangDetectException  # For detecting the language of the input text
import datetime  # For generating timestamps when saving progress

# Initializing the skill extraction pipeline using a pre-trained model
token_skill_classifier = pipeline(
    model="jjzha/escoxlmr_skill_extraction",  # Specifies the model used for extracting skills
    aggregation_strategy="first"  # Aggregates token-level predictions into entity-level ones
)

# Initializing the knowledge extraction pipeline using another pre-trained model
token_knowledge_classifier = pipeline(
    model="jjzha/escoxlmr_knowledge_extraction",  # Specifies the model used for extracting knowledge
    aggregation_strategy="first"  # Aggregates token-level predictions into entity-level ones
)

# Function to extract a substring from text based on start and end indices
def extract_text(text, start, end):
    """
    Extract text from the original text based on start and end indices.
    
    :param text: The full input text (e.g., job description).
    :param start: The starting index of the substring to be extracted.
    :param end: The ending index of the substring to be extracted.
    :return: The extracted substring from the input text.
    """
    return text[start:end + 1]  # Adding 1 to the end index ensures that the character at the 'end' index is included

# Function to aggregate and clean up consecutive token spans from the NER model output
def aggregate_span(results, text):
    new_results = []  # List to store the final aggregated results
    current_result = results[0]  # Initialize with the first result from the model output

    # Iterate over the remaining results
    for result in results[1:]:
        # If the current token is adjacent to the previous token (i.e., end of one token + 1 is the start of the next)
        if result["start"] == current_result["end"] + 1:
            current_text = extract_text(text, result["start"], result["end"])  # Extract the text of the current token

            # Check if the extracted text contains a comma (which may indicate multiple items)
            if ',' in current_text:
                # Split the text by commas and append each part separately
                parts = [part.strip() for part in current_text.split(',')]  # Strips whitespace from each part
                for part in parts:
                    if part:  # Ensure that empty or whitespace-only parts are ignored
                        new_results.append(part)  # Append each cleaned part to the final result list
            else:
                # If there's no comma, concatenate the current token text with the previous one
                current_result["word"] += " " + current_text.strip()  # Add the current text to the previous result
                current_result["end"] = result["end"]  # Update the end index of the current result
        else:
            # If tokens are not adjacent, finalize the previous result and start a new one
            if current_result["word"].strip():  # Ensure that we don't add empty or whitespace-only results
                new_results.append(current_result["word"])  # Append the finalized result
            current_result = result  # Move to the next result

    # After the loop, add the last remaining result if it's valid
    if current_result["word"].strip():
        new_results.append(current_result["word"])

    return new_results  # Return the aggregated and cleaned results

# Function to perform Named Entity Recognition (NER) for both skills and knowledge
def ner(text, lang):
    # Run the skill extraction model on the input text
    output_skills = token_skill_classifier(text)
    print(f'output_skills: {output_skills}')
    
    # Modify the output of the skill model to mark entities as "Skill"
    for result in output_skills:
        if result.get("entity_group"):  # If an entity group exists in the result (which groups tokens)
            result["entity"] = "Skill"  # Rename the entity group to "Skill"
            del result["entity_group"]  # Remove the original entity group field

    # Run the knowledge extraction model on the input text
    output_knowledge = token_knowledge_classifier(text)
    print(f'output_knowledge: {output_knowledge}')

    # Modify the output of the knowledge model to mark entities as "Knowledge"
    for result in output_knowledge:
        if result.get("entity_group"):  # If an entity group exists in the result (which groups tokens)
            result["entity"] = "Knowledge"  # Rename the entity group to "Knowledge"
            del result["entity_group"]  # Remove the original entity group field

    # If there are any skills detected, aggregate their spans
    if len(output_skills) > 0:
        output_skills = aggregate_span(output_skills, text)

    # If there are any knowledge entities detected, aggregate their spans
    if len(output_knowledge) > 0:
        output_knowledge = aggregate_span(output_knowledge, text)

    # Print the number of knowledge and skill entities detected (for debugging purposes)
    print(len(output_knowledge), len(output_skills))
    print(output_knowledge, output_skills)  # Print the actual entities (for debugging purposes)

    # Return a dictionary containing the text, skills, knowledge, and detected language
    return {"text": text, "skills": output_skills, "knowledge": output_knowledge, "detected-language": lang}

# Function to detect the language of the input text
def detect_language(text: str) -> str:
    """
    Detect the language of a given text. Handles empty or erroneous inputs.
    
    :param text: The input text for language detection.
    :return: The language code ('english', 'dutch', 'Other' for other languages, or 'unknown' if detection fails).
    """
    try:
        # Detect the language of the text using the 'detect' function from langdetect
        lang = detect(text)
        if lang == 'en':  # If the language is detected as English
            return 'english'
        elif lang == 'nl':  # If the language is detected as Dutch
            return 'dutch'
        else:  # For any other detected language
            return 'Other'
    except LangDetectException:
        # Return 'unknown' if language detection fails (e.g., gibberish or empty text)
        return 'unknown'
    except TypeError:
        # Return 'unknown' if the text is not a valid string (e.g., NaN or non-text data)
        return 'unknown'

# Main function to perform ESCO skill and knowledge extraction from job descriptions
def initiate_esco_analysis(input_file: str, output_file: str, output_subfolder: str):
    # Load the CSV file containing job descriptions into a pandas DataFrame
    csv_file = input_file
    df = pd.read_csv(csv_file, encoding='utf-8')  # Reads the CSV into a DataFrame
    total_count = df["Description"].count()  # Get the total number of job descriptions
    print(total_count)  # Print the total count (for debugging)

    results = []  # Initialize an empty list to store results for each job description

    # Loop through each job description in the DataFrame
    for i in range(total_count):
        job_description = df["Description"].iloc[i]  # Get the job description at index 'i'
        language = detect_language(job_description)  # Detect the language of the job description

        # Perform Named Entity Recognition (NER) on the job description
        piped = ner(job_description, language)
        results.append(piped)  # Append the result to the results list

        # Save progress every 10% of total job descriptions or when processing the last item
        if (i + 1) % (total_count // 10) == 0 or i == total_count - 1:
            df_results = pd.DataFrame(results)  # Convert the results list to a DataFrame

            # Get the current timestamp for uniquely naming progress files
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

            # Create a filename that indicates the percentage of progress and timestamp
            progress_file = f'{output_subfolder}/extracted_skills_{(i + 1) * 100 // total_count}_{timestamp}.csv'
            
            # Save the intermediate progress as a CSV file
            df_results.to_csv(progress_file, index=False, encoding='utf-8-sig')
            print(f'Saved progress to {progress_file} at {((i + 1) * 100) // total_count}% completion')

    # Final save after processing all job descriptions
    df_results = pd.DataFrame(results)  # Convert the final results to a DataFrame
    df_results.to_csv(output_file, index=False, encoding='utf-8-sig')  # Save the final results to the output file
    print(df_results)  # Print the final DataFrame (for debugging)


