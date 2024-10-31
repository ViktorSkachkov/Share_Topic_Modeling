import os
import sys
import datetime

''' Determining the names of all the folders which are needed for the code as well as for the output folders and files: '''

# Determine the name of the folder in which the package 'Esco_Extractor' is stored. The default is 'my_Packages'.
packages_folder = 'my_Packages'

# Determine the name of the folder in which the data is stored. The default is 'Data'.
data_folder = 'Data'

# Determine the name of the dataset which would be cleaned and which should be stored inside 'Data'. The default is 'final_dataset.csv'.
input_file_name = 'final_dataset.csv'

''' The processes which are needed for the experiment to be conducted: '''

# Get the absolute path of the current script or current working directory
def get_current_directory():
    """Retrieve the current directory, handling script or interactive environments."""
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.getcwd()

# Print the current directory (for debugging)
current_dir = get_current_directory()
print(f"Current Directory: {current_dir}")

# Define a function to find a folder containing a specific target folder or file
def find_folder(starting_dir, target_folder):
    """Search for a target folder in the directory hierarchy."""
    current_dir = starting_dir
    while current_dir != os.path.dirname(current_dir):  # Traverse upwards until root
        potential_folder_path = os.path.join(current_dir, target_folder)
        if os.path.exists(potential_folder_path):
            return potential_folder_path
        current_dir = os.path.dirname(current_dir)  # Move one level up
    return None

# Find the folder where the package is stored dynamically
package_root_dir = find_folder(current_dir, packages_folder)

# If the folder for packages is found, append it to sys.path
if package_root_dir:
    sys.path.append(package_root_dir)
    print(f"Package Path: {package_root_dir}")
else:
    print(f"Error: '{packages_folder}' folder not found.")
    raise FileNotFoundError(f"Could not find '{packages_folder}' folder.")

# Now import the esco_extractor after adding the package path to sys.path
try:
    from Esco_Extractor import esco_extractor
except ImportError as e:
    print(f"Error importing 'Esco_Extractor': {e}")
    raise ImportError("Failed to import 'Esco_Extractor'.")

# Find the 'Data' folder dynamically
data_folder_dir = find_folder(current_dir, data_folder)

# If 'Data' folder is found, proceed
if data_folder_dir:
    print(f"Data folder found: {data_folder_dir}")
else:
    print(f"Error: '{data_folder}' folder not found.")
    raise FileNotFoundError(f"Could not find '{data_folder}' folder.")

# Generate a timestamp for the output subfolder name
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_subfolder = os.path.join(data_folder_dir, f'esco_extracted_features_{timestamp}')

# Ensure the timestamped subfolder exists for outputs
os.makedirs(output_subfolder, exist_ok=True)
print(f"Output subfolder created: {output_subfolder}")

# Define input files in the root of the Data folder
input_file = os.path.join(data_folder_dir, input_file_name)

# Check if the input file exists
if not os.path.isfile(input_file):
    print(f"Error: Input file '{input_file}' not found.")
    raise FileNotFoundError(f"Input file '{input_file}' does not exist.")

# Print input file and obfuscation keys paths for debugging
print(f"Input File: {input_file}")

# Define the output file path in the timestamped subfolder with a timestamp in the name
output_file = os.path.join(output_subfolder, f'esco_all_findings_{timestamp}.csv')

# Print the output file path with the timestamp
print(f"Output File: {output_file}")

# Call the esco_extractor function with the paths
esco_extractor(input_file, output_file, output_subfolder)

# Print completion message
print("Process completed.")