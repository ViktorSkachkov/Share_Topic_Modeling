from .nmf_algorithm_code import NMFModel
from .nmf_visualisation_code import NMFModelVisualizer
import pandas as pd

def topic_modeling_initializer(input_file: str, metrics_file: str, output_subfolder: str, english_stopwords_file: str,
                               dutch_stopwords_file: str, custom_stopwords_file: str, model_file: str, epochs: int, num_top_words: int, num_topics: int):

    # Read input file
    data = pd.read_csv(input_file)
    
    stopword_files = [custom_stopwords_file, dutch_stopwords_file, english_stopwords_file]

    # Initialize and run the NMF Model
    nmf_model = NMFModel(num_topics, data, stopword_files, num_top_words, epochs, output_subfolder)
    nmf_model.fit()

    nmf_model.save_topics(output_subfolder)

    # Evaluate model
    coherence_score, perplexity_score = nmf_model.evaluate()
    nmf_diversity = nmf_model.topic_diversity()
    nmf_hierarchy_quality = nmf_model.hierarchy_quality()
    nmf_silhouette = nmf_model.clustering()
    
    # Prepare the metrics for saving
    metrics = {
        "NMF Coherence": coherence_score,
        "Perplexity": perplexity_score,
        "Diversity": nmf_diversity,
        "NMF Silhouette": nmf_silhouette,
        "Hierarchy Quality": nmf_hierarchy_quality,
    }
    
    with open(metrics_file, 'w') as f:
        f.write("NMF Evaluation Metrics:\n")
        f.write("=========================\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    print(f"Metrics saved to {metrics_file}")