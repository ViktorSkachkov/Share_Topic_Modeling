import os
import sys
import datetime

''' Determining the names of all the folders which are needed for the code as well as for the output folders and files: '''

# Determine the name of the folder in which the package 'Cleaning_Dataset_Pipeline' is stored. The default is 'my_Packages'.
packages_folder = 'my_Packages'

# Determine the name of the folder in which the data is stored. The default is 'Data'.
data_folder = 'Data'

# Determine the name of the dataset which would be cleaned and which should be stored inside 'Data'. The default is 'asam2.csv'.
input_file_name = 'asam2.csv'

# Determine the name of the folder in which the key files are stored. The default is 'Keys'.
keys_folder = 'Keys'

# Determine the name of the subfolder in which the common words are stored inside the folder for keys. The default is 'Common_Words'.
common_words_subfolder = 'Common_Words'

# Determine the name of the subfolder in which the replacements are stored inside the folder for keys. The default is 'Replacements_For_Cleaning_Pipeline'.
replacements_for_cleaning_pipeline_subfolder = 'Replacements_For_Cleaning_Pipeline'

# Determine the name of the subfolder in which the replacements for obfuscating the dataset are stored inside the folder for keys. 
# The default is 'Replacements_For_Cleaning'.
obfuscation_subfolder = 'Replacements_For_Cleaning'

# Determine the name of the file for replacements. The default is 'replacements2.json'.
replacements_name = 'replacements2.json'

# Determine the name of the obfuscations file. The default is 'combined_data_final.json'.
obfuscations_file_name = 'combined_data_final.json'

# Determine the name of the file with English stop words. The default is 'stop_words_english.txt'.
stop_words_english_name = 'stop_words_english.txt'

# Determine the name of the file with Dutch stop words. The default is 'stop_words_dutch.txt'.
stop_words_dutch_name = 'stop_words_dutch.txt'

# Determine the name of the file with Common stop words. The default is 'stop_words_common.txt'.
stop_words_common_name = 'stop_words_common.txt'

''' The processes which are needed for the experiment to be conducted: '''

# Get the absolute path of the current script or current working directory if running interactively
def get_current_directory():
    """Retrieve the current directory, whether running in a script or interactively."""
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.getcwd()

# Print the current directory (for debugging)
current_dir = get_current_directory()
print(f"Current Directory: {current_dir}")

# Define a function to find a folder containing a specific target folder or file (like 'my_Packages', 'Keys', etc.)
def find_folder(starting_dir, target_folder):
    """Search for a target folder by traversing up the directory tree."""
    current_dir = starting_dir
    while current_dir != os.path.dirname(current_dir):  # Traverse upwards until root
        potential_folder_path = os.path.join(current_dir, target_folder)
        if os.path.exists(potential_folder_path):
            return potential_folder_path
        current_dir = os.path.dirname(current_dir)  # Move one level up
    return None

# Find the folder where the package is stored dynamically
package_root_dir = find_folder(current_dir, packages_folder)

# If the folder for the packages is found, append it to sys.path
if package_root_dir:
    sys.path.append(package_root_dir)  # Add the correct folder to sys.path
    print(f"Package Path: {package_root_dir}")
else:
    print(f"Error: {packages_folder} folder not found.")
    sys.exit(1)

# Now import the clean_dataset_pipeline after adding the package path to sys.path
try:
    from Cleaning_Dataset_Pipeline import clean_dataset_pipeline3
except ImportError as e:
    print(f"Error importing 'Cleaning_Dataset_Pipeline': {e}")
    sys.exit(1)

# Find the 'Data' folder dynamically
data_folder_dir = find_folder(current_dir, data_folder)

# If 'Data' folder is found, proceed
if data_folder_dir:
    print(f"{data_folder} folder found: {data_folder_dir}")
else:
    print(f"Error: {data_folder} folder not found.")
    sys.exit(1)

# Generate a timestamp for the output subfolder name
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_subfolder = os.path.join(data_folder_dir, f'cleaning_data_{timestamp}')

# Ensure the timestamped subfolder exists for outputs
os.makedirs(output_subfolder, exist_ok=True)
print(f"Output subfolder created: {output_subfolder}")

# Define input file in the root of the Data folder
input_file = os.path.join(data_folder_dir, input_file_name)

# Ensure the input file exists
if not os.path.isfile(input_file):
    print(f"Error: Input file '{input_file}' not found.")
    sys.exit(1)

# Print input file for debugging
print(f"Input File: {input_file}")

# Define the output file path in the timestamped subfolder with a timestamp in the name
output_file = os.path.join(output_subfolder, f'final_dataset_{timestamp}.csv')

# Print the output file path with the timestamp
print(f"Output File: {output_file}")

# Define a function to find specific folders inside 'Keys'
def find_specific_folder(starting_dir, target_folder):
    """Search for a specific subfolder inside the 'Keys' folder."""
    keys_folder_name = find_folder(current_dir, keys_folder)
    if keys_folder_name:
        # Look for specific target folders
        specific_folder_path = os.path.join(keys_folder_name, target_folder)
        if os.path.exists(specific_folder_path):
            return specific_folder_path
    return None

# Find a specific folder 
common_words_subfolder_dir = find_specific_folder(current_dir, common_words_subfolder)

# If 'Common_Words' is found, proceed
if common_words_subfolder_dir:
    print(f"Common_Words folder found: {common_words_subfolder_dir}")
else:
    print("Error: 'Common_Words' folder not found.")
    sys.exit(1)

# Construct the full paths to the English stop words file
stop_words_english = os.path.join(common_words_subfolder_dir, stop_words_english_name)

# Print English Common Words file path for debugging
print(f"English Common Words File: {stop_words_english}")

# Construct the full paths to the Dutch stop words file
stop_words_dutch = os.path.join(common_words_subfolder_dir, stop_words_dutch_name)

# Print Dutch Common Words file path for debugging
print(f"Dutch Common Words File: {stop_words_dutch}")

# Construct the full paths to the Custom stop words file
stop_words_custom = os.path.join(common_words_subfolder_dir, stop_words_common_name)

# Print Custom Common Words file path for debugging
print(f"Custom Common Words File: {stop_words_custom}")

stopword_files = [stop_words_english, stop_words_dutch, stop_words_custom]

# Find a specific folder
replacements_folder_dir = find_specific_folder(current_dir, replacements_for_cleaning_pipeline_subfolder)

# If the folder is found, proceed
if replacements_folder_dir:
    print(f"{replacements_for_cleaning_pipeline_subfolder} folder found: {replacements_folder_dir}")
else:
    print(f"Error: '{replacements_for_cleaning_pipeline_subfolder}' folder not found.")
    sys.exit(1)

# Construct the full paths to the replacements file
replacements_file_dir = os.path.join(replacements_folder_dir, replacements_name)

# Find the specific folder
obfuscation_subfolder_dir = find_specific_folder(current_dir, obfuscation_subfolder)

# If the subfolder with obfuscations is found, proceed
if obfuscation_subfolder_dir:
    print(f"{obfuscation_subfolder} folder found: {obfuscation_subfolder_dir}")
else:
    print(f"Error: {obfuscation_subfolder} folder not found.")
    sys.exit(1)

# Construct the full paths to the English stop words file
obfuscations_file = os.path.join(obfuscation_subfolder_dir, obfuscations_file_name)

# Call the cleaning function with the paths
try:
    clean_dataset_pipeline3(input_file, output_file, output_subfolder, stopword_files, replacements_file_dir, obfuscations_file)
    print("Cleaning process completed successfully.")
except Exception as e:
    print(f"Error during the cleaning process: {e}")
    sys.exit(1)