"""
Configuration settings for the Whisper Diarization SDK.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WhisperConfig:
    """Configuration for Whisper model settings."""
    
    model_name: str = "medium.en"
    language: Optional[str] = None
    task: str = "transcribe"
    suppress_numerals: bool = True
    temperature: float = 0.0
    compression_ratio_threshold: float = 2.4
    logprob_threshold: float = -1.0
    no_speech_threshold: float = 0.6


@dataclass
class DiarizationConfig:
    """Configuration for speaker diarization settings."""
    
    min_speakers: int = 1
    max_speakers: int = 10
    min_speaker_duration: float = 0.5
    clustering_threshold: float = 0.7
    embedding_batch_size: int = 32


@dataclass
class AudioConfig:
    """Configuration for audio processing settings."""
    
    sample_rate: int = 16000
    chunk_length: float = 30.0
    overlap_length: float = 1.0
    device: str = "auto"
    batch_size: int = 0


@dataclass
class SDKConfig:
    """Main configuration class for the SDK."""
    
    whisper: WhisperConfig
    diarization: DiarizationConfig
    audio: AudioConfig
    
    def __post_init__(self):
        """Initialize default configurations if not provided."""
        if self.whisper is None:
            self.whisper = WhisperConfig()
        if self.diarization is None:
            self.diarization = DiarizationConfig()
        if self.audio is None:
            self.audio = AudioConfig()
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'SDKConfig':
        """Create configuration from dictionary."""
        whisper_config = WhisperConfig(**config_dict.get('whisper', {}))
        diarization_config = DiarizationConfig(**config_dict.get('diarization', {}))
        audio_config = AudioConfig(**config_dict.get('audio', {}))
        
        return cls(
            whisper=whisper_config,
            diarization=diarization_config,
            audio=audio_config
        )
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            'whisper': {
                'model_name': self.whisper.model_name,
                'language': self.whisper.language,
                'task': self.whisper.task,
                'suppress_numerals': self.whisper.suppress_numerals,
                'temperature': self.whisper.temperature,
                'compression_ratio_threshold': self.whisper.compression_ratio_threshold,
                'logprob_threshold': self.whisper.logprob_threshold,
                'no_speech_threshold': self.whisper.no_speech_threshold
            },
            'diarization': {
                'min_speakers': self.diarization.min_speakers,
                'max_speakers': self.diarization.max_speakers,
                'min_speaker_duration': self.diarization.min_speaker_duration,
                'clustering_threshold': self.diarization.clustering_threshold,
                'embedding_batch_size': self.diarization.embedding_batch_size
            },
            'audio': {
                'sample_rate': self.audio.sample_rate,
                'chunk_length': self.audio.chunk_length,
                'overlap_length': self.audio.overlap_length,
                'device': self.audio.device,
                'batch_size': self.audio.batch_size
            }
        }


# Default configuration
DEFAULT_CONFIG = SDKConfig(
    whisper=WhisperConfig(),
    diarization=DiarizationConfig(),
    audio=AudioConfig()
)
