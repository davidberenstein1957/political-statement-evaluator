"""
Whisper Diarization SDK

A Python SDK for Automatic Speech Recognition with Speaker Diarization
based on OpenAI Whisper and NeMo toolkit.
"""

__version__ = "0.1.0"
__author__ = "Mahmoud Ashraf"
__email__ = "mahmoud.ashraf97@gmail.com"

from .config import (
    DEFAULT_CONFIG,
    AudioConfig,
    DiarizationConfig,
    SDKConfig,
    WhisperConfig,
)
from .core import WhisperDiarizer
from .models import DiarizationResult, SpeakerSegment, TranscriptionSegment

__all__ = [
    "WhisperDiarizer",
    "DiarizationResult", 
    "SpeakerSegment",
    "TranscriptionSegment",
    "SDKConfig",
    "WhisperConfig",
    "DiarizationConfig", 
    "AudioConfig",
    "DEFAULT_CONFIG",
    "__version__",
    "__author__",
    "__email__"
]
