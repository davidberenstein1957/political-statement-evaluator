# Political Statement Analysis SDK

A comprehensive Python SDK for analyzing political statements, interviews, and discussions using Large Language Models (LLMs) via LiteLLM.

## Overview

This SDK provides a clean, Pythonic interface to analyze political content for:

- **Critical Questioning Patterns**: Identify hard-hitting vs. soft questions
- **Biased Language Detection**: Find potentially biased adjectives and language
- **Sentiment Analysis**: Analyze sentiment towards political entities
- **Multi-language Support**: Works with Dutch, English, German, French, Spanish, and more
- **Flexible LLM Backend**: Support for OpenAI, Claude, and custom models via LiteLLM

## Features

- 🔍 **Question Analysis**: Categorize questions as critical, confirming, or neutral
- 🎯 **Bias Detection**: Identify potentially biased language and adjectives
- 😊 **Sentiment Analysis**: Analyze sentiment towards political entities
- 🌍 **Multi-language**: Support for multiple languages
- 🤖 **LLM Agnostic**: Works with any model supported by LiteLLM
- 🏠 **Local Models**: Support for LMStudio and other local LLM endpoints
- 📊 **Structured Results**: Clean data models for easy integration
- 🚀 **Simple API**: Easy-to-use Python interface

## Installation

### Prerequisites

- Python 3.10+
- UV package manager (recommended)

### Install the SDK

```bash
# Clone this repository
git clone <your-repo-url>
cd political-statement-evaluator

# Install dependencies using UV
uv sync

# Install in development mode
uv pip install -e .
```

## Quick Start

### Using OpenAI

```python
from political_analysis_sdk import PoliticalStatementAnalyzer

# Initialize with OpenAI
analyzer = PoliticalStatementAnalyzer(
    model_name="gpt-4",
    api_key="your-openai-api-key",
    language="English",
    temperature=0.1
)

# Analyze text
result = analyzer.analyze_text("Your political text here...")

# Access results
print(f"Total questions: {result.total_questions}")
print(f"Critical questions: {result.critical_questions}")
print(f"Summary: {result.summary}")
```

### Using LMStudio (Local Models)

```python
from political_analysis_sdk import PoliticalStatementAnalyzer

# Initialize with LMStudio
analyzer = PoliticalStatementAnalyzer(
    model_name="openai/gpt-oss-20b",  # Custom model name
    base_url="http://localhost:1234/v1",  # LMStudio endpoint
    language="English",
    temperature=0.1
)

# Analyze text
result = analyzer.analyze_text("Your political text here...")
```

## LMStudio Integration

The SDK supports custom model names from LMStudio and other local LLM endpoints:

### Setup LMStudio

1. Download and install [LMStudio](https://lmstudio.ai/)
2. Load your preferred model (e.g., GPT-OSS-20B, Llama-2, etc.)
3. Start the local server on port 1234

### Example LMStudio Usage

```python
# Test LMStudio connection
python examples/test_lmstudio.py

# Run full analysis with LMStudio
python examples/lmstudio_example.py
```

### Supported Model Names

You can use any model name that LMStudio supports, such as:

- `openai/gpt-oss-20b`
- `meta-llama/Llama-2-7b-chat-hf`
- `meta-llama/Llama-2-13b-chat-hf`
- `microsoft/DialoGPT-medium`
- `tiiuae/falcon-7b-instruct`

## API Reference

### PoliticalStatementAnalyzer

Main class for analyzing political statements.

#### Constructor

```python
PoliticalStatementAnalyzer(
    model_name: str = "gpt-4",
    api_key: Optional[str] = None,
    language: str = "Dutch",
    temperature: float = 0.1,
    base_url: Optional[str] = None
)
```

#### Methods

- `analyze_text(text: str) -> AnalysisResult`: Analyze text content directly
- `analyze_text_file(file_path: str) -> AnalysisResult`: Analyze text from a file

### AnalysisResult

Structured result containing all analysis data.

#### Properties

- `total_questions`: Total number of questions found
- `critical_questions`: Number of critical questions
- `confirming_questions`: Number of confirming questions
- `biased_adjectives`: List of biased language found
- `entity_sentiments`: Sentiment analysis for entities
- `question_analysis`: Detailed question analysis
- `summary`: Overall analysis summary

## Examples

### Basic Usage

```python
# See examples/simple_usage.py
python examples/simple_usage.py
```

### LMStudio Usage

```python
# See examples/lmstudio_example.py
python examples/lmstudio_example.py
```

### Test LMStudio Connection

```python
# See examples/test_lmstudio.py
python examples/test_lmstudio.py
```

## Environment Variables

You can configure the SDK using environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export POLITICAL_ANALYSIS_MODEL="gpt-4"
export POLITICAL_ANALYSIS_TEMPERATURE="0.1"
export POLITICAL_ANALYSIS_LANGUAGE="English"
export POLITICAL_ANALYSIS_BASE_URL="http://localhost:1234/v1"
```

## Troubleshooting

### LMStudio Issues

1. **Connection Error**: Make sure LMStudio is running on `http://localhost:1234`
2. **Model Not Found**: Verify the model is loaded in LMStudio
3. **API Error**: Check that the local server is accessible

### General Issues

1. **Import Error**: Make sure you're in the correct directory and dependencies are installed
2. **API Key Error**: Verify your API key is set correctly
3. **Model Error**: Check that the model name is supported by your endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
