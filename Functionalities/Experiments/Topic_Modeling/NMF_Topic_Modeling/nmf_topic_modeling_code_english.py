import os
import sys
import datetime

def get_current_directory():
    return os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

# Print the current directory (for debugging)
current_dir = get_current_directory()
print(f"Current Directory: {current_dir}")

# Efficient folder search
def find_folder_upwards(starting_dir, target_folder):
    current_path = starting_dir
    while True:
        if target_folder in os.listdir(current_path):  # Check only the immediate directory level
            return os.path.join(current_path, target_folder)
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break
        current_path = parent_path
    return None

data_folder = find_folder_upwards(current_dir, 'Data')
if not data_folder:
    raise FileNotFoundError(f"Could not find 'Data' folder in {current_dir} or its parent directories.")
print(f"Data folder found: {data_folder}")

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_subfolder = os.path.join(data_folder, f'nmf_topics_data_2000e_15w_20t_{timestamp}')
os.makedirs(output_subfolder, exist_ok=True)
print(f"Output subfolder created: {output_subfolder}")

input_file = os.path.join(data_folder, 'english_job_postings.csv')
if not os.path.isfile(input_file):
    raise FileNotFoundError(f"Input file '{input_file}' does not exist.")
print(f"Input File: {input_file}")

model_file = os.path.join(data_folder, 'nmf_model1.pkl')
if not os.path.isfile(model_file):
    model_file = os.path.join(output_subfolder, f'nmf_model_{timestamp}.pkl')
else:
    print(f"Model file found: {model_file}")

package_root_dir = find_folder_upwards(current_dir, 'my_Packages')
if not package_root_dir:
    raise FileNotFoundError(f"Could not find 'my_Packages' folder in {current_dir} or its parent directories.")
print(f"'my_Packages' found: {package_root_dir}")

topic_modeling_packages_dir = os.path.join(package_root_dir, 'Topic_Modeling_Packages')
if os.path.isdir(topic_modeling_packages_dir) and topic_modeling_packages_dir not in sys.path:
    sys.path.append(topic_modeling_packages_dir)
    print(f"Topic Modeling Package Path: {topic_modeling_packages_dir}")
else:
    raise FileNotFoundError(f"Could not find 'Topic_Modeling_Packages' folder in '{package_root_dir}'.")

try:
    from NMF_Topic_Modeling import topic_modeling_initializer
except ImportError as e:
    raise ImportError(f"Failed to import 'NMF_Topic_Modeling': {e}")

keys_folder = find_folder_upwards(current_dir, 'Keys')
if not keys_folder:
    raise FileNotFoundError(f"Could not find 'Keys' folder in {current_dir} or its parent directories.")
print(f"Keys folder found: {keys_folder}")

common_words_folder = os.path.join(keys_folder, 'Common_Words')
if not os.path.isdir(common_words_folder):
    raise FileNotFoundError(f"Could not find 'Common_Words' folder in '{keys_folder}'.")
print(f"Common_Words folder found: {common_words_folder}")

stop_words_english = os.path.join(common_words_folder, 'stop_words_english.txt')
stop_words_dutch = os.path.join(common_words_folder, 'stop_words_dutch.txt')
stop_words_custom = os.path.join(common_words_folder, 'stop_words_custom.txt')

for stop_words_file in [stop_words_english, stop_words_dutch, stop_words_custom]:
    if not os.path.isfile(stop_words_file):
        raise FileNotFoundError(f"Stop words file '{stop_words_file}' does not exist.")
print(f"Stop Words files found: English, Dutch, and Custom")

output_file = os.path.join(output_subfolder, f'nmf_topics_2000e_15w_20t_{timestamp}.txt')
print(f"Output File: {output_file}")

# Create a file to save metrics
metrics_file = os.path.join(output_subfolder, f'nmf_metrics_2000e_15w_20t_{timestamp}.txt')
print(f"Metrics File: {metrics_file}")

epochs = 2000
num_top_words = 15
num_topics = 20

topic_modeling_initializer(input_file, metrics_file, output_subfolder, stop_words_english, stop_words_dutch, stop_words_custom, model_file, epochs, num_top_words, num_topics)
print("Process completed.")