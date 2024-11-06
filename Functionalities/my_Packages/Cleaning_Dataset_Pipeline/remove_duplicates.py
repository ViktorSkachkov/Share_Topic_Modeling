import pandas as pd
from itertools import combinations
import os

class JobPostDeduplicator:
    def __init__(self, output_subfolder: str, output_txt: str = "output_txt_file_removed_duplicates.txt", output_csv: str = "removed_rows_duplicates.csv"):
        """
        Initializes the JobPostDeduplicator object by accepting a DataFrame and folder path for output files, and optional file names.
        
        Parameters:
        - output_subfolder: Folder where the additional output files (TXT and CSV) should be saved.
        - output_txt: Name of the text file that will store duplicate information (default: "output_txt_file_removed_duplicates.txt").
        - output_csv: Name of the CSV file that will store the removed duplicates (default: "removed_rows_duplicates.csv").
        """
        self.similar_rows = []  # List to store groups of similar rows
        self.output_subfolder = output_subfolder  # Folder to save additional output files
        self.removed_rows = pd.DataFrame()  # DataFrame to store removed rows

        # Ensure the output folder exists, if not, create it
        os.makedirs(output_subfolder, exist_ok=True)

        # Set full paths for the additional output files
        self.output_txt = os.path.join(output_subfolder, output_txt)
        self.output_csv = os.path.join(output_subfolder, output_csv)

    def are_similar(self, text1, text2):
        """
        Compares two strings (text1, text2) to determine if they are exactly the same.
        
        Parameters:
        - text1: First string for comparison
        - text2: Second string for comparison
        
        Returns:
        - Boolean: True if the texts are exactly the same, False otherwise.
        """
        return text1 == text2

    def find_duplicates(self):
        """
        Identifies rows in the DataFrame that are similar based on the 'Description' and 'Title' columns.
        It iterates over all pairs of rows and groups the indices of rows that are at least 95% similar
        in both columns.
        
        The results are stored as sets in the self.similar_rows list, where each set contains the row indices 
        that are considered duplicates of each other.
        """
        description_title_pairs = self.df[['Description', 'Title']].values  # Extract the values of 'Description' and 'Title'
        row_combinations = combinations(range(len(self.df)), 2)  # Get all possible row pairs
        
        duplicate_groups = []  # List to store sets of duplicate row indices
        
        # Loop through each pair of rows
        for i, j in row_combinations:
            desc1, title1 = description_title_pairs[i]  # Row i's 'Description' and 'Title'
            desc2, title2 = description_title_pairs[j]  # Row j's 'Description' and 'Title'
            
            # Check if both the 'Description' and 'Title' fields are similar
            if self.are_similar(desc1, desc2) and self.are_similar(title1, title2):
                # If similarity is found, check if they are already in a duplicate group
                added_to_group = False
                for group in duplicate_groups:
                    if i in group or j in group:
                        # If either row is already in a group, add the other row to the same group
                        group.update([i, j])
                        added_to_group = True
                        break
                
                # If neither row is in any existing group, create a new group
                if not added_to_group:
                    duplicate_groups.append(set([i, j]))
        
        # Save the grouped duplicate rows in the object
        self.similar_rows = duplicate_groups

    def save_duplicate_info(self):
        """
        Writes the information about duplicate rows to a text file. Each line in the file
        contains the indices of rows that are similar to each other.
        """
        with open(self.output_txt, 'w') as f:
            for group in self.similar_rows:
                # Convert set of row indices to a sorted list and write it to the file
                f.write(f"Duplicate group: {sorted(list(group))}\n")

    def remove_duplicates(self):
        """
        Removes duplicate rows from the DataFrame, keeping only one row per group of duplicates.
        The method identifies which rows should be dropped based on the duplicate groups found earlier,
        and stores those removed rows for later saving.
        """
        rows_to_drop = set()  # Set to store row indices that will be removed
        
        for group in self.similar_rows:
            # For each group of duplicates, keep only the first row and drop the others
            rows_to_drop.update(sorted(group)[1:])  # Drop all but the first row
        
        # Store the removed rows in the removed_rows DataFrame
        self.removed_rows = self.df.loc[list(rows_to_drop)]
        
        # Drop the identified rows from the DataFrame
        self.df = self.df.drop(list(rows_to_drop)).reset_index(drop=True)

    def save_removed_rows_csv(self):
        """
        Saves the removed rows (duplicates) DataFrame to a CSV file.
        """
        self.removed_rows.to_csv(self.output_csv, index=False, encoding='utf-8-sig')

    def deduplicate_and_save(self, df: pd.DataFrame):
        """
        The main function that orchestrates the deduplication process. 
        It finds duplicate rows, saves the duplicate information to a text file, 
        removes duplicates from the DataFrame, and finally returns the cleaned DataFrame.
        """
        
        self.df = df  # Input DataFrame

        # Step 1: Deduplication process
        self.find_duplicates()  # Find duplicate rows
        self.save_duplicate_info()  # Save duplicate row indices to a text file
        self.remove_duplicates()  # Remove duplicate rows from the DataFrame
        self.save_removed_rows_csv()  # Save the removed rows to the CSV file
        
        print("Removal of duplicates completed.")
        return self.df  # Return the deduplicated DataFrame