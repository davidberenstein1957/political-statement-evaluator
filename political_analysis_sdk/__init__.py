"""
Political Statement Analysis SDK

A comprehensive toolkit for analyzing political statements, interviews, and discussions
to identify critical questioning patterns, biased language, and sentiment analysis.
"""

from political_analysis_sdk.cli import main as cli_main
from political_analysis_sdk.config import Config
from political_analysis_sdk.core import PoliticalStatementAnalyzer
from political_analysis_sdk.models import (
    AnalysisResult,
    BiasAnalysis,
    QuestionAnalysis,
    SentimentAnalysis,
)
from political_analysis_sdk.prompts import PromptTemplates
from political_analysis_sdk.utils import parse_srt_file, save_text_file

__version__ = "0.1.0"
__all__ = [
    "PoliticalStatementAnalyzer",
    "AnalysisResult",
    "QuestionAnalysis",
    "BiasAnalysis",
    "SentimentAnalysis",
    "PromptTemplates",
    "Config",
    "cli_main",
    "parse_srt_file",
    "save_text_file",
]
