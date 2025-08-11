#!/usr/bin/env python3
"""
Simple usage example for the Political Statement Analysis SDK.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the SDK
sys.path.append(str(Path(__file__).parent.parent))

from political_analysis_sdk import PoliticalStatementAnalyzer
from political_analysis_sdk.utils import parse_srt_file


def main():
    # Initialize the analyzer with local API server
    local_analyzer = PoliticalStatementAnalyzer(
        model_name="gpt-4o-mini",  # Model name from your API
        language="Dutch",
        temperature=0.1

    )
    print("✓ Local API analyzer initialized")
    print(f"Model: {local_analyzer.model_name}")
    print(f"Base URL: {local_analyzer.base_url}")

    # Sample political text for analysis
    sample_text = parse_srt_file("data/cafe-kockelmann-cafe-kockelmann_21-2025-02-28.srt")

    print("\nAnalyzing political statement text...")
    print("=" * 50)

    try:
        # Use local API analyzer for the example
        result = local_analyzer.analyze_text(sample_text)

        # Display results
        print("Analysis completed successfully!")
        print(f"Text file: {result.text_file_path}")
        print(f"Total questions found: {result.total_questions}")
        print(f"Critical questions: {result.critical_questions}")
        print(f"Confirming questions: {result.confirming_questions}")
        print(f"Biased adjectives found: {len(result.biased_adjectives)}")
        print(f"Entities analyzed: {len(result.entity_sentiments)}")

        print("\n" + "=" * 50)
        print("DETAILED RESULTS:")
        print("=" * 50)

        # Question analysis
        if result.question_analysis:
            print("\nQUESTION ANALYSIS:")
            for i, question in enumerate(result.question_analysis, 1):
                print(f"{i}. Type: {question.question_type.value}")
                print(f"   Question: {question.question_text}")
                print(f"   Context: {question.context}")
                print(f"   Reasoning: {question.reasoning}")
                print(f"   Confidence: {question.confidence:.2f}")
                print()

        # Bias analysis
        if result.biased_adjectives:
            print("BIAS ANALYSIS:")
            for i, bias in enumerate(result.biased_adjectives, 1):
                print(f"{i}. Adjective: {bias.adjective}")
                print(f"   Target: {bias.target_person}")
                print(f"   Bias type: {bias.bias_type}")
                print(f"   Context: {bias.context}")
                print(f"   Reasoning: {bias.reasoning}")
                print(f"   Confidence: {bias.confidence:.2f}")
                print()

        # Sentiment analysis
        if result.entity_sentiments:
            print("SENTIMENT ANALYSIS:")
            for i, sentiment in enumerate(result.entity_sentiments, 1):
                print(f"{i}. Entity: {sentiment.entity_name}")
                print(f"   Type: {sentiment.entity_type}")
                print(f"   Sentiment: {sentiment.sentiment.value}")
                print(f"   Context: {sentiment.context}")
                print(f"   Reasoning: {sentiment.reasoning}")
                print(f"   Confidence: {sentiment.confidence:.2f}")
                if sentiment.supporting_quotes:
                    print(f"   Supporting quotes: {', '.join(sentiment.supporting_quotes)}")
                print()

        # Summary
        print("=" * 50)
        print("SUMMARY:")
        print("=" * 50)
        print(result.summary)

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
