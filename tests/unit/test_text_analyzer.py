"""Tests for the TextAnalyzer tool."""

import pytest

from claude_tools.tools.text_analyzer import TextAnalyzer


class TestTextAnalyzer:
    """Test cases for TextAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create a TextAnalyzer instance for testing."""
        return TextAnalyzer()

    @pytest.fixture
    def sample_text(self):
        """Sample text for testing."""
        return """This is a sample text for testing.
        It has multiple lines and sentences. The text analyzer should
        be able to count words, lines, and sentences correctly!
        This is the fourth line."""

    @pytest.fixture
    def sample_file(self, tmp_path, sample_text):
        """Create a temporary text file for testing."""
        file_path = tmp_path / "test.txt"
        file_path.write_text(sample_text)
        return file_path

    def test_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.name == "text_analyzer"
        assert analyzer.version == "0.1.0"
        assert len(analyzer.stop_words) > 0

    def test_validate_inputs_with_text(self, analyzer):
        """Test input validation with text parameter."""
        assert analyzer.validate_inputs(text="sample") is True

    def test_validate_inputs_with_file(self, analyzer, sample_file):
        """Test input validation with file parameter."""
        assert analyzer.validate_inputs(file_path=str(sample_file)) is True

    def test_validate_inputs_missing_params(self, analyzer):
        """Test input validation with missing parameters."""
        assert analyzer.validate_inputs() is False

    def test_validate_inputs_nonexistent_file(self, analyzer):
        """Test input validation with non-existent file."""
        assert analyzer.validate_inputs(file_path="/nonexistent/file.txt") is False

    def test_execute_with_text(self, analyzer, sample_text):
        """Test execution with direct text input."""
        result = analyzer.execute(text=sample_text)

        assert "basic_stats" in result
        assert result["basic_stats"]["words"] == 31
        assert (
            result["basic_stats"]["sentences"] == 4
        )  # 4 sentences ending with . and !
        assert result["basic_stats"]["lines"] == 4

        assert "word_analysis" in result
        assert result["word_analysis"]["unique_words"] > 0
        assert len(result["word_analysis"]["most_common_words"]) <= 10

        assert "sentence_analysis" in result
        assert result["sentence_analysis"]["average_sentence_length"] > 0

    def test_execute_with_file(self, analyzer, sample_file):
        """Test execution with file input."""
        result = analyzer.execute(file_path=str(sample_file))

        assert result["basic_stats"]["words"] == 31
        assert result["basic_stats"]["sentences"] == 4

    def test_execute_without_stop_words(self, analyzer):
        """Test execution filtering stop words."""
        text = "The quick brown fox jumps over the lazy dog"
        result = analyzer.execute(text=text, include_stop_words=False)

        # Check that common words like "the" are filtered
        common_words = [w["word"] for w in result["word_analysis"]["most_common_words"]]
        assert "the" not in common_words
        assert (
            "quick" in common_words or "brown" in common_words or "fox" in common_words
        )

    def test_execute_with_stop_words(self, analyzer):
        """Test execution including stop words."""
        text = "The the the fox fox dog"
        result = analyzer.execute(text=text, include_stop_words=True)

        # "the" should be the most common word
        assert result["word_analysis"]["most_common_words"][0]["word"] == "the"
        assert result["word_analysis"]["most_common_words"][0]["count"] == 3

    def test_execute_custom_top_words(self, analyzer):
        """Test execution with custom top words count."""
        text = "one two three four five six seven eight nine ten eleven twelve"
        result = analyzer.execute(text=text, top_words_count=5)

        assert len(result["word_analysis"]["most_common_words"]) == 5

    def test_execute_empty_text(self, analyzer):
        """Test execution with empty text."""
        result = analyzer.execute(text="")

        assert result["basic_stats"]["words"] == 0
        assert result["basic_stats"]["sentences"] == 0
        assert result["word_analysis"]["vocabulary_richness"] == 0

    def test_execute_invalid_inputs(self, analyzer):
        """Test execution with invalid inputs."""
        with pytest.raises(ValueError, match="Invalid inputs"):
            analyzer.execute()
