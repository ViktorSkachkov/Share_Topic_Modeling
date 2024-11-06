import pandas as pd

class InvalidDataRemover:
    def __init__(self, output_subfolder: str, removed_rows_file: str = "removed_rows_invalid_data.csv"):
        """
        Initialize the cleaner with the folder path for output and the file name for removed rows.
        
        :param output_subfolder: Folder path where the removed rows and cleaned data will be saved.
        :param removed_rows_file: File name to save the removed rows.
        """
        self.data = None
        self.output_subfolder = output_subfolder
        self.removed_rows_file = removed_rows_file
        self.removed_rows = None  # DataFrame to hold removed rows
    
    def filter_descriptions(self, min_length: int = 30):
        """
        Remove rows where the 'Description' column has 30 characters or less.

        :param min_length: Minimum length of the job description (default is 30 characters).
        """
        if self.data is not None:
            # Identify rows to be removed
            self.removed_rows = self.data[self.data['Description'].str.len() <= min_length]
            # Filter out the rows with valid descriptions
            self.data = self.data[self.data['Description'].str.len() > min_length]
        else:
            raise ValueError("There is a problem with the DataFrame.")
    
    def save_cleaned_data(self, df: pd.DataFrame):
        """
        Save the cleaned dataset to a new CSV file and store removed rows in a separate file.

        :param df: DataFrame containing job postings to clean.
        :return: The cleaned DataFrame.
        """
        self.data = df
        self.filter_descriptions()  # Filter out invalid descriptions

        # Save removed rows to the specified output subfolder and file
        if self.removed_rows is not None and not self.removed_rows.empty:
            removed_rows_path = f"{self.output_subfolder}/{self.removed_rows_file}"
            self.removed_rows.to_csv(removed_rows_path, index=False)

        print("Removal of invalid data completed.")

        # Return the cleaned DataFrame
        return self.data
