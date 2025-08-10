"""
Data models for political statement analysis results.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List


class SentimentType(Enum):
    """Enumeration for sentiment types."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class QuestionType(Enum):
    """Enumeration for question types."""
    CRITICAL = "critical"
    CONFIRMING = "confirming"
    FOLLOW_UP = "follow_up"
    NEUTRAL = "neutral"


@dataclass
class QuestionAnalysis:
    """Analysis results for question patterns."""
    question_text: str
    question_type: QuestionType
    confidence: float
    reasoning: str
    context: str


@dataclass
class BiasAnalysis:
    """Analysis results for biased language usage."""
    adjective: str
    target_person: str
    bias_type: str
    confidence: float
    reasoning: str
    context: str


@dataclass
class SentimentAnalysis:
    """Analysis results for sentiment towards entities."""
    entity_name: str
    entity_type: str  # person, company, party
    sentiment: SentimentType
    confidence: float
    reasoning: str
    context: str
    supporting_quotes: List[str]


@dataclass
class AnalysisResult:
    """Complete analysis result for a political statement text."""
    text_file_path: str
    total_questions: int
    critical_questions: int
    confirming_questions: int
    biased_adjectives: List[BiasAnalysis]
    entity_sentiments: List[SentimentAnalysis]
    question_analysis: List[QuestionAnalysis]
    summary: str
    metadata: Dict[str, Any]
