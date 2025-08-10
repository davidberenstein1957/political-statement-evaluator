"""
Basic tests for the Political Statement Analysis SDK.
"""

import sys
from pathlib import Path

import pytest

# Add the parent directory to the path so we can import the SDK
sys.path.append(str(Path(__file__).parent.parent))

from political_analysis_sdk import PoliticalStatementAnalyzer
from political_analysis_sdk.models import QuestionType, SentimentType


class TestPoliticalStatementAnalyzer:
    """Test class for the PoliticalStatementAnalyzer."""
    
    def test_analyzer_initialization(self):
        """Test that the analyzer can be initialized."""
        analyzer = PoliticalStatementAnalyzer()
        assert analyzer.model_name == "gpt-4"
        assert analyzer.language == "Dutch"
        assert analyzer.temperature == 0.1
    
    def test_analyzer_with_custom_params(self):
        """Test analyzer initialization with custom parameters."""
        analyzer = PoliticalStatementAnalyzer(
            model_name="gpt-3.5-turbo",
            language="English",
            temperature=0.5
        )
        assert analyzer.model_name == "gpt-3.5-turbo"
        assert analyzer.language == "English"
        assert analyzer.temperature == 0.5
    
    def test_question_type_enum(self):
        """Test that question types are properly defined."""
        assert QuestionType.CRITICAL == "critical"
        assert QuestionType.CONFIRMING == "confirming"
        assert QuestionType.FOLLOW_UP == "follow_up"
        assert QuestionType.NEUTRAL == "neutral"
    
    def test_sentiment_type_enum(self):
        """Test that sentiment types are properly defined."""
        assert SentimentType.POSITIVE == "positive"
        assert SentimentType.NEGATIVE == "negative"
        assert SentimentType.NEUTRAL == "neutral"
        assert SentimentType.MIXED == "mixed"


if __name__ == "__main__":
    pytest.main([__file__])
