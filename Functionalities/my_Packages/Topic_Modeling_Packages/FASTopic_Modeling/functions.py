from .fast_algorithm_code import TopicModelingPipeline
from .fast_algorithm_vocabulary_code import TopicModelingPipelineVocabulary
from .fast_visualisation_code import TopicModelingVisualisation

def topic_modeling_initializer(input_file: str, output_file: str, output_subfolder: str, english_stopwords_file: str,
                               dutch_stopwords_file: str, custom_stopwords_file: str, model_file: str, epochs: int, num_top_words: int, num_topics: int):
    print(english_stopwords_file)
    print(dutch_stopwords_file)
    print(custom_stopwords_file)
    
    # stopword_files = [custom_stopwords_file, english_stopwords_file, dutch_stopwords_file]
    topic_modeling_pipeline = TopicModelingPipeline(input_file, model_file, output_file, custom_stopwords_file, english_stopwords_file, dutch_stopwords_file, output_subfolder, num_topics, num_top_words, epochs)
    topic_modeling_pipeline.run()

def topic_modeling_initializer_with_vocabulary(input_file: str, output_file: str, output_subfolder: str, english_stopwords_file: str,
                               dutch_stopwords_file: str, custom_stopwords_file: str, model_file: str, epochs: int, num_top_words: int, num_topics: int, vocabulary_file: str):
    print(english_stopwords_file)
    print(dutch_stopwords_file)
    print(custom_stopwords_file)
    
    # stopword_files = [custom_stopwords_file, english_stopwords_file, dutch_stopwords_file]
    topic_modeling_pipeline = TopicModelingPipelineVocabulary(input_file, model_file, output_file, custom_stopwords_file, english_stopwords_file, dutch_stopwords_file, output_subfolder, num_topics, num_top_words, epochs, vocabulary_file)
    topic_modeling_pipeline.run()