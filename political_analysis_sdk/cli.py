#!/usr/bin/env python3
"""
Command-line interface for the Political Statement Analysis SDK.
"""

import argparse
import json
import sys
from pathlib import Path

from political_analysis_sdk.config import Config
from political_analysis_sdk.core import PoliticalStatementAnalyzer


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Analyze political statements for critical questions, bias, and sentiment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a text file
  python -m political_analysis_sdk.cli analyze-file interview.txt

  # Analyze text directly
  python -m political_analysis_sdk.cli analyze-text "Sample political text here"

  # Use custom model and language
  python -m political_analysis_sdk.cli analyze-file interview.txt --model gpt-3.5-turbo --language English

  # Output results to JSON file
  python -m political_analysis_sdk.cli analyze-file interview.txt --output results.json
        """
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Analyze file command
    file_parser = subparsers.add_parser('analyze-file', help='Analyze a text file')
    file_parser.add_argument('file_path', help='Path to the text file to analyze')

    # Analyze text command
    text_parser = subparsers.add_parser('analyze-text', help='Analyze text directly')
    text_parser.add_argument('text', help='Text content to analyze')

    # Common options for both commands
    for subparser in [file_parser, text_parser]:
        subparser.add_argument(
            '--model', '-m',
            default=Config.DEFAULT_MODEL,
            choices=Config.get_supported_models(),
            help=f'LLM model to use (default: {Config.DEFAULT_MODEL})'
        )
        subparser.add_argument(
            '--language', '-l',
            default=Config.DEFAULT_LANGUAGE,
            choices=Config.get_supported_languages(),
            help=f'Language for analysis (default: {Config.DEFAULT_LANGUAGE})'
        )
        subparser.add_argument(
            '--temperature', '-t',
            type=float,
            default=Config.DEFAULT_TEMPERATURE,
            help=f'Temperature for LLM responses (default: {Config.DEFAULT_TEMPERATURE})'
        )
        subparser.add_argument(
            '--output', '-o',
            help='Output file for results (JSON format)'
        )
        subparser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Verbose output'
        )

    # List supported models and languages
    subparsers.add_parser('list-models', help='List supported LLM models')
    subparsers.add_parser('list-languages', help='List supported languages')

    return parser


def analyze_file(file_path: str, args: argparse.Namespace) -> dict:
    """Analyze a text file."""
    analyzer = PoliticalStatementAnalyzer(
        model_name=args.model,
        language=args.language,
        temperature=args.temperature
    )

    result = analyzer.analyze_text_file(file_path)
    return result_to_dict(result)


def analyze_text(text: str, args: argparse.Namespace) -> dict:
    """Analyze text directly."""
    analyzer = PoliticalStatementAnalyzer(
        model_name=args.model,
        language=args.language,
        temperature=args.temperature
    )

    result = analyzer.analyze_text(text)
    return result_to_dict(result)


def result_to_dict(result) -> dict:
    """Convert AnalysisResult to dictionary for JSON output."""
    return {
        'text_file_path': result.text_file_path,
        'total_questions': result.total_questions,
        'critical_questions': result.critical_questions,
        'confirming_questions': result.confirming_questions,
        'biased_adjectives': [
            {
                'adjective': b.adjective,
                'target_person': b.target_person,
                'bias_type': b.bias_type,
                'confidence': b.confidence,
                'reasoning': b.reasoning,
                'context': b.context
            }
            for b in result.biased_adjectives
        ],
        'entity_sentiments': [
            {
                'entity_name': s.entity_name,
                'entity_type': s.entity_type,
                'sentiment': s.sentiment.value,
                'confidence': s.confidence,
                'reasoning': s.reasoning,
                'context': s.context,
                'supporting_quotes': s.supporting_quotes
            }
            for s in result.entity_sentiments
        ],
        'question_analysis': [
            {
                'question_text': q.question_text,
                'question_type': q.question_type.value,
                'confidence': q.confidence,
                'reasoning': q.reasoning,
                'context': q.context
            }
            for q in result.question_analysis
        ],
        'summary': result.summary,
        'metadata': result.metadata
    }


def print_results(results: dict, args: argparse.Namespace):
    """Print analysis results to console."""
    if args.verbose:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("Analysis completed successfully!")
        print(f"Total questions: {results['total_questions']}")
        print(f"Critical questions: {results['critical_questions']}")
        print(f"Confirming questions: {results['confirming_questions']}")
        print(f"Biased adjectives found: {len(results['biased_adjectives'])}")
        print(f"Entities analyzed: {len(results['entity_sentiments'])}")
        print(f"\nSummary:\n{results['summary']}")


def save_results(results: dict, output_file: str):
    """Save results to output file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to: {output_file}")


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == 'analyze-file':
            if not Path(args.file_path).exists():
                print(f"Error: File not found: {args.file_path}")
                sys.exit(1)

            results = analyze_file(args.file_path, args)
            print_results(results, args)

            if args.output:
                save_results(results, args.output)

        elif args.command == 'analyze-text':
            results = analyze_text(args.text, args)
            print_results(results, args)

            if args.output:
                save_results(results, args.output)

        elif args.command == 'list-models':
            print("Supported LLM models:")
            for model in Config.get_supported_models():
                print(f"  - {model}")

        elif args.command == 'list-languages':
            print("Supported languages:")
            for language in Config.get_supported_languages():
                print(f"  - {language}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
