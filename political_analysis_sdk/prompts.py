"""
Prompt templates for political statement analysis using LLMs.
"""

from typing import Any, Dict


class PromptTemplates:
    """Collection of adaptable prompt templates for political analysis."""

    @staticmethod
    def get_question_analysis_prompt(text: str, language: str = "Dutch") -> str:
        """Generate prompt for analyzing question patterns."""
        return f"""Analyzeer de volgende tekst in het {language} en identificeer alle vragen.
        Classificeer elke vraag als:
        - "critical": Kritische wedervragen die uitdagen of in twijfel trekken
        - "confirming": Bevestigende follow-up vragen die bevestigen
        - "follow_up": Neutrale follow-up vragen voor verduidelijking
        - "neutral": Gewone neutrale vragen

        Tekst:
        {text}

        BELANGRIJK: Geef je antwoord ALLEEN in geldig JSON formaat, zonder extra tekst ervoor of erna.
        {{
            "questions": [
                {{
                    "question": "de vraag tekst",
                    "type": "critical|confirming|follow_up|neutral",
                    "confidence": 0.95,
                    "reasoning": "waarom deze classificatie",
                    "context": "context rond de vraag"
                }}
            ]
        }}

        Als er geen vragen zijn gevonden, geef dan: {{"questions": []}}"""

    @staticmethod
    def get_bias_analysis_prompt(text: str, language: str = "Dutch") -> str:
        """Generate prompt for analyzing biased language."""
        return f"""Analyzeer de volgende tekst in het {language} en identificeer alle niet-neutrale,
        kwalificerende bijvoeglijke naamwoorden die worden gebruikt om personen te beschrijven.

        Zoek naar woorden die een oordeel, vooroordeel of bias uitdrukken.

        Tekst:
        {text}

        BELANGRIJK: Geef je antwoord ALLEEN in geldig JSON formaat, zonder extra tekst ervoor of erna.
        {{
            "biased_adjectives": [
                {{
                    "adjective": "het bijvoeglijk naamwoord",
                    "target_person": "naam van de persoon",
                    "bias_type": "positief/negatief/pejoratief/etc",
                    "confidence": 0.95,
                    "reasoning": "waarom dit biased is",
                    "context": "context van gebruik"
                }}
            ]
        }}

        Als er geen biased bijvoeglijke naamwoorden zijn gevonden, geef dan: {{"biased_adjectives": []}}"""

    @staticmethod
    def get_sentiment_analysis_prompt(text: str, language: str = "Dutch") -> str:
        """Generate prompt for analyzing sentiment towards entities."""
        return f"""Analyzeer de volgende tekst in het {language} en identificeer alle
        uitspraken over bedrijven, partijen en personen. Bepaal of er positief,
        negatief of neutraal over wordt gesproken.

        Tekst:
        {text}

        BELANGRIJK: Geef je antwoord ALLEEN in geldig JSON formaat, zonder extra tekst ervoor of erna.
        {{
            "entity_sentiments": [
                {{
                    "entity_name": "naam van entiteit",
                    "entity_type": "person|company|party",
                    "sentiment": "positive|negative|neutral|mixed",
                    "confidence": 0.95,
                    "reasoning": "waarom deze sentiment",
                    "context": "context van de uitspraak",
                    "supporting_quotes": ["quote 1", "quote 2"]
                }}
            ]
        }}

        Als er geen entiteiten zijn gevonden, geef dan: {{"entity_sentiments": []}}"""

    @staticmethod
    def get_summary_prompt(analysis_results: Dict[str, Any], language: str = "Dutch") -> str:
        """Generate prompt for creating a summary of all analysis results."""
        return f"""Maak een samenvatting van de volgende analyse resultaten in het {language}:

        Vragen Analyse:
        - Totaal aantal vragen: {analysis_results.get('total_questions', 0)}
        - Kritische vragen: {analysis_results.get('critical_questions', 0)}
        - Bevestigende vragen: {analysis_results.get('confirming_questions', 0)}

        Bias Analyse:
        - Aantal gevonden biased bijvoeglijke naamwoorden: {len(analysis_results.get('biased_adjectives', []))}

        Sentiment Analyse:
        - Aantal geanalyseerde entiteiten: {len(analysis_results.get('entity_sentiments', []))}

        Geef een beknopte samenvatting van de belangrijkste bevindingen en patronen die je ziet in deze tekst."""
