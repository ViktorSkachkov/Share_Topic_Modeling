from .esco_extraction import initiate_esco_analysis

def esco_extractor(input_file: str, output_file: str, output_subfolder: str):
    initiate_esco_analysis(input_file, output_file, output_subfolder)