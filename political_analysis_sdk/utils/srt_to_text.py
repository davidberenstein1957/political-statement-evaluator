#!/usr/bin/env python3
"""
Script to convert SRT subtitle files to plain text.
Extracts only the text content, removing timestamps and subtitle numbers.
"""

import argparse
import sys
from pathlib import Path
from typing import List


def parse_srt_file(srt_path: Path) -> str:
    """
    Parse an SRT file and extract text content, merging all lines.

    Args:
        srt_path: Path to the SRT file

    Returns:
        Merged text content as a single string
    """
    if isinstance(srt_path, str):
        srt_path = Path(srt_path)

    if not srt_path.exists():
        raise FileNotFoundError(f"SRT file not found: {srt_path}")

    text_lines: List[str] = []

    try:
        with open(srt_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # SRT format: number, timestamp, text, blank line (repeats)
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Skip subtitle number
            if line.isdigit():
                i += 1
                continue

            # Skip timestamp line (contains -->)
            if '-->' in line:
                i += 1
                continue

            # Skip empty lines
            if not line:
                i += 1
                continue

                        # This should be text content
            text_lines.append(line)
            i += 1

    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(srt_path, 'r', encoding='latin-1') as file:
                lines = file.readlines()

            i = 0
            while i < len(lines):
                line = lines[i].strip()

                if line.isdigit():
                    i += 1
                    continue

                if '-->' in line:
                    i += 1
                    continue

                if not line:
                    i += 1
                    continue

                text_lines.append(line)
                i += 1

        except Exception as e:
            raise RuntimeError(f"Failed to read SRT file with multiple encodings: {e}")

    # Merge all text lines into one continuous string
    merged_text = ' '.join(text_lines)
    return merged_text


def save_text_file(text_content: str, output_path: Path) -> None:
    """
    Save text content to a file.

    Args:
        text_content: Text content to save
        output_path: Path for the output text file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
    except Exception as e:
        raise RuntimeError(f"Failed to write output file: {e}")


def main() -> None:
    """Main function to handle command line arguments and execute conversion."""
    parser = argparse.ArgumentParser(
        description="Convert SRT subtitle files to plain text",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python srt_to_text.py input.srt                    # Convert to input.txt
  python srt_to_text.py input.srt -o output.txt      # Specify output file
  python srt_to_text.py input.srt --stdout           # Print to stdout
        """
    )

    parser.add_argument(
        'input_file',
        type=str,
        help='Input SRT file path'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output text file path (default: input_file.txt)'
    )

    parser.add_argument(
        '--stdout',
        action='store_true',
        help='Print output to stdout instead of saving to file'
    )

    args = parser.parse_args()

    try:
        # Parse input file
        input_path = Path(args.input_file)
        text_content = parse_srt_file(input_path)

        if not text_content:
            print("Warning: No text content found in SRT file", file=sys.stderr)
            return

        # Handle output
        if args.stdout:
            # Print to stdout
            print(text_content)
        else:
            # Save to file
            if args.output:
                output_path = Path(args.output)
            else:
                # Default: replace .srt with .txt
                output_path = input_path.with_suffix('.txt')

            save_text_file(text_content, output_path)
            print(f"Successfully converted {input_path} to {output_path}")
            print(f"Extracted {len(text_content.split())} words")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
