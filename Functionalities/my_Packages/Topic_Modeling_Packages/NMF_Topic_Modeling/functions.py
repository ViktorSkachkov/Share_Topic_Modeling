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

    nmf_topic_coherence = nmf_model.calculate_topic_coherence()
    nmf_topic_diversity = nmf_model.calculate_topic_diversity()
    nmf_silhouette_score = nmf_model.calculate_silhouette_score()
    nmf_clustering_stability = nmf_model.evaluate_clustering_stability()
    nmf_cosine_similarity = nmf_model.calculate_cosine_similarity()

    # Get and print metrics
    print("Topic Coherence:", nmf_topic_coherence)
    print("Topic Diversity:", nmf_topic_diversity)
    print("Silhouette Score:", nmf_silhouette_score)
    print("Clustering Stability Score:", nmf_clustering_stability)
    print("Cosine Similarity Score:", nmf_cosine_similarity)

    # Save metrics to a text file
    with open(metrics_file, 'w') as f:
        f.write("NMF Model Metrics\n")
        f.write("=================\n")
        f.write(f"Topic Coherence: {nmf_topic_coherence:.4f}\n")
        f.write(f"Topic Diversity: {nmf_topic_diversity:.4f}\n")
        f.write(f"Silhouette Score: {nmf_silhouette_score:.4f}\n")
        f.write(f"Clustering Stability Score: {nmf_clustering_stability:.4f}\n")
        f.write("Cosine Similarity Matrix:\n")
        f.write(f"{nmf_cosine_similarity}\n")

    print(f"Metrics saved to {metrics_file}")

    # After calculating the metrics
    visualizer = NMFModelVisualizer(nmf_model, output_subfolder)
    visualizer.create_all_visualizations(
        nmf_topic_coherence, 
        nmf_topic_diversity, 
        nmf_silhouette_score, 
        nmf_clustering_stability, 
        nmf_cosine_similarity
)