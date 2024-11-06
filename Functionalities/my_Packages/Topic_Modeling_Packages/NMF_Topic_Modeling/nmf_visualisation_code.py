import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np

class NMFModelVisualizer:
    def __init__(self, nmf_model, output_subfolder):
        self.nmf_model = nmf_model
        self.output_subfolder = output_subfolder

    def visualize_topics(self):
        # Generate word clouds for each topic
        topics = self.nmf_model.display_topics()
        for i, topic in enumerate(topics):
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(topic))
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f"Word Cloud for Topic {i + 1}")
            plt.savefig(os.path.join(self.output_subfolder, f"wordcloud_topic_{i + 1}.png"))
            plt.close()
        print("Word clouds saved.")

    def visualize_topic_coherence(self, topic_coherence):
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.bar(['Coherence Score'], [topic_coherence], color='blue')
        plt.title('Coherence Score')
        plt.ylim(0, max(1, topic_coherence + 0.1))

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_subfolder, 'coherence.png'))
        plt.close()  # Close the figure after saving

    def visualize_topic_diversity(self, topic_diversity):
        plt.figure(figsize=(5, 5))
        # Visualize single float as a bar plot
        plt.bar(['Diversity Score'], [topic_diversity], color='green')
        plt.ylabel('Diversity Score')
        plt.title('Topic Diversity')
        plt.savefig(os.path.join(self.output_subfolder, 'topic_diversity.png'))
        plt.close()
        print("Topic diversity visualization saved.")

    def visualize_silhouette_score(self, silhouette_score):
        plt.figure(figsize=(5, 5))
        # Visualize single float as a bar plot
        plt.bar(['Silhouette Score'], [silhouette_score], color='orange')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score')
        plt.savefig(os.path.join(self.output_subfolder, 'silhouette_score.png'))
        plt.close()
        print("Silhouette score visualization saved.")

    def visualize_clustering_stability(self, clustering_stability):
        plt.figure(figsize=(5, 5))
        # Visualize single float as a bar plot
        plt.bar(['Clustering Stability'], [clustering_stability], color='purple')
        plt.ylabel('Stability Score')
        plt.title('Clustering Stability Score')
        plt.savefig(os.path.join(self.output_subfolder, 'clustering_stability.png'))
        plt.close()
        print("Clustering stability visualization saved.")

    def visualize_cosine_similarity(self, cosine_similarity):
        plt.figure(figsize=(30, 24))
        sns.heatmap(cosine_similarity, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, square=True)
        plt.title('Cosine Similarity Matrix')
        plt.savefig(os.path.join(self.output_subfolder, 'cosine_similarity_heatmap.png'))
        plt.close()
        print("Cosine similarity heatmap saved.")

    def create_all_visualizations(self, topic_coherence, topic_diversity, silhouette_score, clustering_stability, cosine_similarity):
        self.visualize_topics()
        self.visualize_topic_coherence(topic_coherence)
        self.visualize_topic_diversity(topic_diversity)
        self.visualize_silhouette_score(silhouette_score)
        self.visualize_clustering_stability(clustering_stability)
        self.visualize_cosine_similarity(cosine_similarity)