"""Text file analyzer tool for analyzing text content."""

import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Optional

from claude_tools.core.base_tool import BaseTool


class TextAnalyzer(BaseTool):
    """Analyzes text files for various metrics and statistics.

    This tool provides comprehensive text analysis including:
    - Character, word, and line counts
    - Most common words
    - Sentence analysis
    - Readability metrics
    """

    def __init__(self) -> None:
        """Initialize the text analyzer tool."""
        super().__init__(
            name="text_analyzer",
            description="Analyzes text files for metrics and statistics",
            version="0.1.0",
        )
        self.stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "was",
            "are",
            "were",
            "been",
            "be",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "them",
            "their",
            "what",
            "which",
            "who",
            "when",
            "where",
            "why",
            "how",
            "all",
            "each",
            "every",
        }

    def validate_inputs(self, **kwargs) -> bool:
        """Validate the inputs for text analysis.

        Args:
            **kwargs: Should contain either 'file_path' or 'text'

        Returns:
            True if inputs are valid, False otherwise
        """
        if "file_path" not in kwargs and "text" not in kwargs:
            self.logger.error("Must provide either 'file_path' or 'text' parameter")
            return False

        if "file_path" in kwargs and kwargs["file_path"] is not None:
            file_path = Path(kwargs["file_path"])
            if not file_path.exists():
                self.logger.error(f"File not found: {file_path}")
                return False
            if not file_path.is_file():
                self.logger.error(f"Path is not a file: {file_path}")
                return False

        return True

    def execute(
        self,
        file_path: Optional[str] = None,
        text: Optional[str] = None,
        include_stop_words: bool = False,
        top_words_count: int = 10,
        **kwargs,
    ) -> Dict[str, Any]:
        """Analyze text content and return statistics.

        Args:
            file_path: Path to text file to analyze
            text: Direct text content to analyze
            include_stop_words: Whether to include stop words in word frequency
            top_words_count: Number of most common words to return
            **kwargs: Additional optional parameters

        Returns:
            Dictionary containing analysis results
        """
        # Build validation kwargs only with non-None values
        validation_kwargs = {}
        if file_path is not None:
            validation_kwargs["file_path"] = file_path
        if text is not None:
            validation_kwargs["text"] = text

        if not self.validate_inputs(**validation_kwargs):
            raise ValueError("Invalid inputs provided")

        # Get text content
        if file_path:
            self.logger.info(f"Reading text from file: {file_path}")
            with open(file_path, encoding="utf-8") as f:
                content = f.read()
        else:
            content = text or ""

        # Basic counts
        char_count = len(content)
        char_count_no_spaces = len(
            content.replace(" ", "").replace("\n", "").replace("\t", "")
        )
        line_count = content.count("\n") + (
            1 if content and not content.endswith("\n") else 0
        )

        # Word analysis
        words = re.findall(r"\b\w+\b", content.lower())
        word_count = len(words)

        # Filter stop words if requested
        if not include_stop_words:
            filtered_words = [w for w in words if w not in self.stop_words]
        else:
            filtered_words = words

        # Word frequency
        word_freq = Counter(filtered_words)
        most_common = word_freq.most_common(top_words_count)

        # Sentence analysis
        sentences = re.split(r"[.!?]+", content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        # Average calculations
        avg_word_length = (
            sum(len(word) for word in words) / word_count if word_count > 0 else 0
        )
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0

        # Unique words
        unique_words = len(set(words))
        vocabulary_richness = unique_words / word_count if word_count > 0 else 0

        return {
            "basic_stats": {
                "characters": char_count,
                "characters_no_spaces": char_count_no_spaces,
                "words": word_count,
                "lines": line_count,
                "sentences": sentence_count,
            },
            "word_analysis": {
                "unique_words": unique_words,
                "vocabulary_richness": round(vocabulary_richness, 3),
                "average_word_length": round(avg_word_length, 2),
                "most_common_words": [
                    {"word": word, "count": count} for word, count in most_common
                ],
            },
            "sentence_analysis": {
                "average_sentence_length": round(avg_sentence_length, 2),
                "shortest_sentence": (
                    min(len(s.split()) for s in sentences) if sentences else 0
                ),
                "longest_sentence": (
                    max(len(s.split()) for s in sentences) if sentences else 0
                ),
            },
            "configuration": {
                "include_stop_words": include_stop_words,
                "top_words_count": top_words_count,
            },
        }
