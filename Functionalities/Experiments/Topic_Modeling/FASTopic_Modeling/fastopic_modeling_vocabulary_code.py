import os
import sys
import datetime

# Get the absolute path of the current script or current working directory
def get_current_directory():
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.getcwd()

# Print the current directory (for debugging)
current_dir = get_current_directory()
print(f"Current Directory: {current_dir}")

# Function to find a specific folder starting from a given directory and moving upwards
def find_folder_upwards(starting_dir, target_folder):
    current_path = starting_dir
    while True:
        # Check for the target folder in the current directory
        for dirpath, dirnames, filenames in os.walk(current_path):
            if target_folder in dirnames:
                return os.path.join(dirpath, target_folder)
        
        # Move up to the parent directory
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:  # If we reach the root directory
            break
        current_path = parent_path
    return None

# Find the 'Data' folder dynamically starting from the current directory
data_folder = find_folder_upwards(current_dir, 'Data')

# If 'Data' folder is found, proceed
if data_folder:
    print(f"Data folder found: {data_folder}")
else:
    print(f"Error: 'Data' folder not found in {current_dir} or its parent directories.")
    raise FileNotFoundError(f"Could not find 'Data' folder in {current_dir} or its parent directories.")

# Generate a timestamp for the output subfolder name
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_subfolder = os.path.join(data_folder, f'fast_topics_data_{timestamp}')

# Ensure the timestamped subfolder exists for outputs
os.makedirs(output_subfolder, exist_ok=True)
print(f"Output subfolder created: {output_subfolder}")

# Define input files in the root of the Data folder
input_file = os.path.join(data_folder, 'english_job_postings.csv')

# Check if the input file exists
if not os.path.isfile(input_file):
    print(f"Error: Input file '{input_file}' not found.")
    raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

# Define model file in the root of the Data folder
model_file = os.path.join(data_folder, 'something.pkl')

# Check if the model file exists
if not os.path.isfile(model_file):
    print(f"Warning: Model file '{model_file}' not found. Setting model_file to another name.")
    model_file = os.path.join(output_subfolder, f'fastopic_model_{timestamp}.pkl')
else:
    print(f"Model file found: {model_file}")

# Find the specific folder 'my_Packages'
package_root_dir = find_folder_upwards(current_dir, 'my_Packages')  # Start searching from the current directory upwards

# If 'my_Packages' is found, append it to sys.path
if package_root_dir:
    # Now search for 'Topic_Modeling_Packages' within 'my_Packages'
    topic_modeling_packages_dir = os.path.join(package_root_dir, 'Topic_Modeling_Packages')
    if os.path.isdir(topic_modeling_packages_dir):
        sys.path.append(topic_modeling_packages_dir)
        print(f"Topic Modeling Package Path: {topic_modeling_packages_dir}")
    else:
        print(f"Error: 'Topic_Modeling_Packages' folder not found in '{package_root_dir}'.")
        raise FileNotFoundError(f"Could not find 'Topic_Modeling_Packages' folder in '{package_root_dir}'.")

else:
    print(f"Error: 'my_Packages' folder not found in {current_dir} or its parent directories.")
    raise FileNotFoundError(f"Could not find 'my_Packages' folder in {current_dir} or its parent directories.")

# Now import the topic_modeling_initializer after adding the package path to sys.path
try:
    from FASTopic_Modeling import topic_modeling_initializer_with_vocabulary
except ImportError as e:
    print(f"Error importing 'FASTopic_Modeling': {e}")
    raise ImportError("Failed to import 'FASTopic_Modeling'.")

# Find the specific folder 'Keys' and then 'Common_Words'
keys_folder = find_folder_upwards(current_dir, 'Keys')  # Start searching for 'Keys' from the current directory upwards

# If 'Keys' folder is found, check for 'Common_Words' inside it
if keys_folder:
    common_words_folder = os.path.join(keys_folder, 'Common_Words')
    if os.path.isdir(common_words_folder):
        print(f"Common_Words folder found: {common_words_folder}")
    else:
        print(f"Error: 'Common_Words' folder not found in '{keys_folder}'.")
        raise FileNotFoundError(f"Could not find 'Common_Words' folder in '{keys_folder}'.")
else:
    print(f"Error: 'Keys' folder not found in {current_dir} or its parent directories.")
    raise FileNotFoundError(f"Could not find 'Keys' folder in {current_dir} or its parent directories.")

# Construct the full paths to the English stop words file
stop_words_english = os.path.join(common_words_folder, 'stop_words_english.txt')

# Check if the stop words file exists
if not os.path.isfile(stop_words_english):
    print(f"Error: Stop words file '{stop_words_english}' not found.")
    raise FileNotFoundError(f"Stop words file '{stop_words_english}' does not exist.")

# Print English Common Words file path for debugging
print(f"English Common Words File: {stop_words_english}")

# Construct the full paths to the Dutch stop words file
stop_words_dutch = os.path.join(common_words_folder, 'stop_words_dutch.txt')

# Check if the stop words file exists
if not os.path.isfile(stop_words_dutch):
    print(f"Error: Stop words file '{stop_words_dutch}' not found.")
    raise FileNotFoundError(f"Stop words file '{stop_words_dutch}' does not exist.")

# Print Dutch Common Words file path for debugging
print(f"Dutch Common Words File: {stop_words_dutch}")

# Construct the full paths to the Custom stop words file
stop_words_custom = os.path.join(common_words_folder, 'stop_words_custom.txt')

# Check if the stop words file exists
if not os.path.isfile(stop_words_custom):
    print(f"Error: Stop words file '{stop_words_custom}' not found.")
    raise FileNotFoundError(f"Stop words file '{stop_words_custom}' does not exist.")

# Print Custom Common Words file path for debugging
print(f"Custom Common Words File: {stop_words_custom}")

# If 'Keys' folder is found, check for 'Common_Words' inside it
if keys_folder:
    vocabulary_words_folder = os.path.join(keys_folder, 'Vocabulary_Words')
    if os.path.isdir(vocabulary_words_folder):
        print(f"Vocabulary_Words folder found: {vocabulary_words_folder}")
    else:
        print(f"Error: 'Vocabulary_Words' folder not found in '{keys_folder}'.")
        raise FileNotFoundError(f"Could not find 'Vocabulary_Words' folder in '{keys_folder}'.")
else:
    print(f"Error: 'Keys' folder not found in {current_dir} or its parent directories.")
    raise FileNotFoundError(f"Could not find 'Keys' folder in {current_dir} or its parent directories.")

# Construct the full paths to the vocabulary file
vocabulary_file = os.path.join(vocabulary_words_folder, 'skill_demand_evolution_vocabulary.txt')

# Check if the stop words file exists
if not os.path.isfile(vocabulary_file):
    print(f"Error: Vocabulary words file '{vocabulary_file}' not found.")
    raise FileNotFoundError(f"Vocabulary words file '{vocabulary_file}' does not exist.")

# Print Vocabulary Words file path for debugging
print(f"Vocabulary Words File: {vocabulary_file}")

# Define the output file path in the timestamped subfolder with a timestamp in the name
output_file = os.path.join(output_subfolder, f'fast_topics_{timestamp}.txt')

# Print the output file path with the timestamp
print(f"Output File: {output_file}")

# epochs = 500
epochs = 2000

num_top_words = 15

num_topics = 20

# Call the cleaning function with the paths
topic_modeling_initializer_with_vocabulary(input_file, output_file, output_subfolder, stop_words_english, stop_words_dutch, stop_words_custom, model_file, epochs, num_top_words, num_topics, vocabulary_file)

# Print completion message
print("Process completed.")