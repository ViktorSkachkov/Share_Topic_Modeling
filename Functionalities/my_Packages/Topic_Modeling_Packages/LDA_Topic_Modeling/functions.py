from .lda_algorithm_code import LDAModel
from .lda_visualisation_code import LDAModelVisualizer
import pandas as pd

def topic_modeling_initializer(input_file: str, metrics_file: str, output_subfolder: str, english_stopwords_file: str,
                               dutch_stopwords_file: str, custom_stopwords_file: str, model_file: str, epochs: int, num_top_words: int, num_topics: int):

    # Read input file
    data = pd.read_csv(input_file)
    
    # Initialize and fit the LDA model
    lda_model = LDAModel(num_topics=num_topics, data=data, stopword_files=[custom_stopwords_file, dutch_stopwords_file, english_stopwords_file], num_top_words=num_top_words, epochs=epochs)
    lda_model.fit()

    lda_model.save_topics(output_subfolder)

    # Evaluate model
    coherence_score, perplexity_score = lda_model.evaluate()
    lda_diversity = lda_model.topic_diversity()
    lda_hierarchy_quality = lda_model.hierarchy_quality()
    lda_silhouette = lda_model.clustering()
    
    # Prepare the metrics for saving
    metrics = {
        "LDA Coherence": coherence_score,
        "Perplexity": perplexity_score,
        "Diversity": lda_diversity,
        "LDA Silhouette": lda_silhouette,
        "Hierarchy Quality": lda_hierarchy_quality,
    }
    
    with open(metrics_file, 'w') as f:
        f.write("LDA Evaluation Metrics:\n")
        f.write("=========================\n")
        for key, value in metrics.items():
            f.write(f"{key}: {value}\n")
    
    print(f"Metrics saved to {metrics_file}")

    # Initialize visualizer and plot
    visualizer = LDAModelVisualizer(lda_model, output_subfolder)
    visualizer.plot_top_words()
    visualizer.plot_coherence_and_perplexity(coherence_score, perplexity_score)
    visualizer.plot_topic_distribution(data)
    visualizer.plot_distance_matrix()
    visualizer.plot_topic_clustering()