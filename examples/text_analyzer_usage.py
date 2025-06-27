"""Example usage of the TextAnalyzer tool."""
import json

from claude_tools.tools.text_analyzer import TextAnalyzer
from claude_tools.utils.logging import setup_logging


def main():
    """Demonstrate how to use the TextAnalyzer tool."""
    # Set up logging
    setup_logging(level="INFO")

    # Create an instance of the analyzer
    analyzer = TextAnalyzer()

    # Get tool information
    info = analyzer.get_info()
    print(f"Tool: {info['name']} v{info['version']}")
    print(f"Description: {info['description']}")
    print("-" * 50)

    # Example 1: Analyze a simple text
    print("\nExample 1: Analyzing a simple text")
    sample_text = """The Python programming language is powerful and versatile.
    It is used for web development, data science, artificial intelligence,
    and many other applications. Python's simple syntax makes it easy to learn.
    The language has a large and active community."""

    result = analyzer.execute(text=sample_text)
    print("Basic Statistics:")
    print(f"  - Words: {result['basic_stats']['words']}")
    print(f"  - Sentences: {result['basic_stats']['sentences']}")
    print(f"  - Unique words: {result['word_analysis']['unique_words']}")
    print(f"  - Vocabulary richness: {result['word_analysis']['vocabulary_richness']}")

    # Example 2: Analyze without stop words
    print("\nExample 2: Most common words (excluding stop words)")
    result = analyzer.execute(
        text=sample_text, include_stop_words=False, top_words_count=5
    )
    print("Top 5 words:")
    for word_data in result["word_analysis"]["most_common_words"]:
        print(f"  - '{word_data['word']}': {word_data['count']} times")

    # Example 3: Analyze with stop words included
    print("\nExample 3: Most common words (including stop words)")
    result = analyzer.execute(
        text=sample_text, include_stop_words=True, top_words_count=5
    )
    print("Top 5 words:")
    for word_data in result["word_analysis"]["most_common_words"]:
        print(f"  - '{word_data['word']}': {word_data['count']} times")

    # Example 4: Detailed analysis
    print("\nExample 4: Detailed analysis")
    detailed_text = """
    Natural language processing (NLP) is a subfield of artificial intelligence.
    NLP focuses on the interaction between computers and human language.
    It involves teaching machines to understand, interpret, and generate human language.
    NLP has many practical applications including chatbots, translation services,
    and sentiment analysis. The field continues to evolve rapidly with advances
    in machine learning and deep learning technologies.
    """

    result = analyzer.execute(text=detailed_text)
    print("\nComplete Analysis:")
    print(json.dumps(result, indent=2))

    # Example 5: Analyze a file (if you create one)
    print("\nExample 5: File analysis")
    # Uncomment and modify the path to analyze an actual file
    # result = analyzer.execute(file_path="/path/to/your/text/file.txt")
    # print(f"File analysis complete: {result['basic_stats']['words']} words found")


if __name__ == "__main__":
    main()
