"""
Core political statement analyzer using LLMs via litellm.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import litellm

from political_analysis_sdk.models import (
    AnalysisResult,
    BiasAnalysis,
    QuestionAnalysis,
    QuestionType,
    SentimentAnalysis,
    SentimentType,
)
from political_analysis_sdk.prompts import PromptTemplates


class PoliticalStatementAnalyzer:
    """
    Main analyzer class for political statements using LLM analysis.
    """

    def __init__(
        self,
        model_name: str = "gpt-4",
        api_key: Optional[str] = None,
        language: str = "Dutch",
        temperature: float = 0.1,
        base_url: Optional[str] = None
    ):
        """
        Initialize the analyzer.

        Args:
            model_name: LLM model to use (default: gpt-4)
            api_key: API key for the LLM service
            language: Language for analysis (default: Dutch)
            temperature: Temperature for LLM responses (default: 0.1 for consistency)
            base_url: Base URL for custom API endpoints (e.g., LMStudio)
        """
        self.model_name = model_name
        self.language = language
        self.temperature = temperature
        self.base_url = base_url

        # Configure litellm
        if api_key:
            litellm.api_key = api_key

        # Configure custom base URL for LMStudio or other local models
        if base_url:
            # For local models like LMStudio, set the base URL
            litellm.api_base = base_url

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def analyze_text_file(self, file_path: str) -> AnalysisResult:
        """
        Analyze a text file containing political statements.

        Args:
            file_path: Path to the text file to analyze

        Returns:
            AnalysisResult containing all analysis data
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read the text file
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()

        self.logger.info(f"Analyzing text file: {file_path}")

        # Perform all analyses
        question_analysis = self._analyze_questions(text_content)
        bias_analysis = self._analyze_bias(text_content)
        sentiment_analysis = self._analyze_sentiment(text_content)

        # Create summary
        summary = self._create_summary({
            'total_questions': len(question_analysis),
            'critical_questions': len([q for q in question_analysis if q.question_type == QuestionType.CRITICAL]),
            'confirming_questions': len([q for q in question_analysis if q.question_type == QuestionType.CONFIRMING]),
            'biased_adjectives': bias_analysis,
            'entity_sentiments': sentiment_analysis
        })

        return AnalysisResult(
            text_file_path=str(file_path),
            total_questions=len(question_analysis),
            critical_questions=len([q for q in question_analysis if q.question_type == QuestionType.CRITICAL]),
            confirming_questions=len([q for q in question_analysis if q.question_type == QuestionType.CONFIRMING]),
            biased_adjectives=bias_analysis,
            entity_sentiments=sentiment_analysis,
            question_analysis=question_analysis,
            summary=summary,
            metadata={
                'model_used': self.model_name,
                'language': self.language,
                'temperature': self.temperature
            }
        )

    def _analyze_questions(self, text: str) -> List[QuestionAnalysis]:
        """Analyze question patterns in the text."""
        prompt = PromptTemplates.get_question_analysis_prompt(text, self.language)

        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            content = response.choices[0].message.content.strip()
            
            # Check if content is empty
            if not content:
                self.logger.warning("Empty response from LLM for question analysis")
                return []
            
            # Try to parse JSON, with fallback handling
            try:
                data = json.loads(content)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse JSON response for questions: {json_error}")
                self.logger.error(f"Raw response content: {content}")
                return []

            questions = []
            for q_data in data.get('questions', []):
                try:
                    question_type = QuestionType(q_data.get('type', 'neutral'))
                    questions.append(QuestionAnalysis(
                        question_text=q_data.get('question', ''),
                        question_type=question_type,
                        confidence=q_data.get('confidence', 0.0),
                        reasoning=q_data.get('reasoning', ''),
                        context=q_data.get('context', '')
                    ))
                except Exception as e:
                    self.logger.warning(f"Error processing question data: {e}")
                    continue

            return questions

        except Exception as e:
            self.logger.error(f"Error analyzing questions: {e}")
            return []

    def _analyze_bias(self, text: str) -> List[BiasAnalysis]:
        """Analyze biased language in the text."""
        prompt = PromptTemplates.get_bias_analysis_prompt(text, self.language)

        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            content = response.choices[0].message.content.strip()
            
            # Check if content is empty
            if not content:
                self.logger.warning("Empty response from LLM for bias analysis")
                return []
            
            # Try to parse JSON, with fallback handling
            try:
                data = json.loads(content)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse JSON response for bias: {json_error}")
                self.logger.error(f"Raw response content: {content}")
                return []

            biases = []
            for b_data in data.get('biased_adjectives', []):
                try:
                    biases.append(BiasAnalysis(
                        adjective=b_data.get('adjective', ''),
                        target_person=b_data.get('target_person', ''),
                        bias_type=b_data.get('bias_type', ''),
                        confidence=b_data.get('confidence', 0.0),
                        reasoning=b_data.get('reasoning', ''),
                        context=b_data.get('context', '')
                    ))
                except Exception as e:
                    self.logger.warning(f"Error processing bias data: {e}")
                    continue

            return biases

        except Exception as e:
            self.logger.error(f"Error analyzing bias: {e}")
            return []

    def _analyze_sentiment(self, text: str) -> List[SentimentAnalysis]:
        """Analyze sentiment towards entities in the text."""
        prompt = PromptTemplates.get_sentiment_analysis_prompt(text, self.language)

        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            content = response.choices[0].message.content.strip()
            
            # Check if content is empty
            if not content:
                self.logger.warning("Empty response from LLM for sentiment analysis")
                return []
            
            # Try to parse JSON, with fallback handling
            try:
                data = json.loads(content)
            except json.JSONDecodeError as json_error:
                self.logger.error(f"Failed to parse JSON response for sentiment: {json_error}")
                self.logger.error(f"Raw response content: {content}")
                return []

            sentiments = []
            for s_data in data.get('entity_sentiments', []):
                try:
                    sentiment = SentimentType(s_data.get('sentiment', 'neutral'))
                    sentiments.append(SentimentAnalysis(
                        entity_name=s_data.get('entity_name', ''),
                        entity_type=s_data.get('entity_type', ''),
                        sentiment=sentiment,
                        confidence=s_data.get('confidence', 0.0),
                        reasoning=s_data.get('reasoning', ''),
                        context=s_data.get('context', ''),
                        supporting_quotes=s_data.get('supporting_quotes', [])
                    ))
                except Exception as e:
                    self.logger.warning(f"Error processing sentiment data: {e}")
                    continue

            return sentiments

        except Exception as e:
            self.logger.error(f"Error analyzing sentiment: {e}")
            return []

    def _create_summary(self, analysis_results: Dict[str, Any]) -> str:
        """Create a summary of all analysis results."""
        prompt = PromptTemplates.get_summary_prompt(analysis_results, self.language)

        try:
            response = litellm.completion(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )

            content = response.choices[0].message.content.strip()
            
            # Check if content is empty
            if not content:
                self.logger.warning("Empty response from LLM for summary creation")
                return "Kon geen samenvatting maken - lege reactie van het model."
            
            return content

        except Exception as e:
            self.logger.error(f"Error creating summary: {e}")
            return "Kon geen samenvatting maken vanwege een fout."

    def analyze_text(self, text: str) -> AnalysisResult:
        """
        Analyze text content directly (without file).

        Args:
            text: Text content to analyze

        Returns:
            AnalysisResult containing all analysis data
        """
        self.logger.info("Analyzing provided text content")

        try:
            # Perform all analyses
            question_analysis = self._analyze_questions(text)
            bias_analysis = self._analyze_bias(text)
            sentiment_analysis = self._analyze_sentiment(text)

            # Create summary
            summary = self._create_summary({
                'total_questions': len(question_analysis),
                'critical_questions': len([q for q in question_analysis if q.question_type == QuestionType.CRITICAL]),
                'confirming_questions': len([q for q in question_analysis if q.question_type == QuestionType.CONFIRMING]),
                'biased_adjectives': bias_analysis,
                'entity_sentiments': sentiment_analysis
            })

            return AnalysisResult(
                text_file_path="direct_text_input",
                total_questions=len(question_analysis),
                critical_questions=len([q for q in question_analysis if q.question_type == QuestionType.CRITICAL]),
                confirming_questions=len([q for q in question_analysis if q.question_type == QuestionType.CONFIRMING]),
                biased_adjectives=bias_analysis,
                entity_sentiments=sentiment_analysis,
                question_analysis=question_analysis,
                summary=summary,
                metadata={
                    'model_used': self.model_name,
                    'language': self.language,
                    'temperature': self.temperature
                }
            )
        except Exception as e:
            self.logger.error(f"Error in analyze_text: {e}")
            # Return a minimal result with error information
            return AnalysisResult(
                text_file_path="direct_text_input",
                total_questions=0,
                critical_questions=0,
                confirming_questions=0,
                biased_adjectives=[],
                entity_sentiments=[],
                question_analysis=[],
                summary=f"Fout tijdens analyse: {str(e)}",
                metadata={
                    'model_used': self.model_name,
                    'language': self.language,
                    'temperature': self.temperature,
                    'error': str(e)
                }
            )
