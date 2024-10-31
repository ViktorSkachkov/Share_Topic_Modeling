import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE


class LDAModelVisualizer:
    def __init__(self, lda_model, output_subfolder):
        self.lda_model = lda_model
        self.output_subfolder = output_subfolder
        
        # Create the output directory if it doesn't exist
        os.makedirs(self.output_subfolder, exist_ok=True)
    
    def plot_top_words(self):
        topics = self.lda_model.display_topics()

        # Create a DataFrame to hold top words for each topic
        top_words_data = {f'Topic {i + 1}': topic for i, topic in enumerate(topics)}
        
        # Create a DataFrame with topics as columns
        df_top_words = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in top_words_data.items()]))
        
        # Save the DataFrame to an Excel file
        excel_path = os.path.join(self.output_subfolder, 'top_words.xlsx')
        df_top_words.to_excel(excel_path, index=False)  # Save to Excel without row indices

    def plot_coherence_and_perplexity(self, coherence_score, perplexity_score):
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.bar(['Coherence Score'], [coherence_score], color='blue')
        plt.title('Coherence Score')
        plt.ylim(0, max(1, coherence_score + 0.1))

        plt.subplot(1, 2, 2)
        plt.bar(['Perplexity Score'], [perplexity_score], color='orange')
        plt.title('Perplexity Score')
        plt.ylim(0, max(1, perplexity_score + 10))
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_subfolder, 'coherence_perplexity.png'))
        plt.close()  # Close the figure after saving

    def plot_topic_distribution(self, data):
        topic_matrix = self.lda_model.model.transform(self.lda_model.doc_term_matrix)
        topic_distribution = topic_matrix.argmax(axis=1)

        plt.figure(figsize=(8, 4))
        sns.countplot(x=topic_distribution, palette='viridis')
        plt.title('Topic Distribution Across Documents')
        plt.xlabel('Topics')
        plt.ylabel('Number of Documents')
        plt.xticks(range(self.lda_model.num_topics))
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_subfolder, 'topic_distribution.png'))
        plt.close()  # Close the figure after saving

    def plot_distance_matrix(self):
        distances = self.lda_model.hierarchy_quality()
        plt.figure(figsize=(32, 16))
        sns.heatmap(distances, annot=True, fmt=".2f", cmap="YlGnBu")
        plt.title("Topic Distance Matrix")
        plt.xlabel("Topics")
        plt.ylabel("Topics")
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_subfolder, 'distance_matrix.png'))
        plt.close()  # Close the figure after saving

    def plot_topic_clustering(self):
        # Get the topic representation from the LDA model
        topic_matrix = self.lda_model.model.transform(self.lda_model.doc_term_matrix)

        # Reduce dimensionality using t-SNE
        tsne = TSNE(n_components=2, random_state=42)
        topic_embeddings = tsne.fit_transform(topic_matrix)

        # Assign a unique color to each topic
        num_topics = self.lda_model.num_topics
        colors = plt.cm.viridis(np.linspace(0, 1, num_topics))  # Generate distinct colors

        # Create a scatter plot with unique colors for each topic
        plt.figure(figsize=(10, 8))
        for i in range(num_topics):
            plt.scatter(topic_embeddings[i, 0], topic_embeddings[i, 1], 
                        color=colors[i], marker='o', s=100, alpha=0.7)

        # Title and labels
        plt.title('Topic Clustering Visualization')
        plt.xlabel('t-SNE Component 1')
        plt.ylabel('t-SNE Component 2')

        # Annotate points with topic numbers
        for i in range(num_topics):
            plt.annotate(f'Topic {i + 1}', (topic_embeddings[i, 0], topic_embeddings[i, 1]), fontsize=12)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_subfolder, 'topic_clustering.png'))
        plt.close()  # Close the figure after saving