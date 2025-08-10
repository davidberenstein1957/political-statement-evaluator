"""
Data models for the Whisper Diarization SDK.
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Dict, List, Optional


@dataclass
class SpeakerSegment:
    """Represents a segment of audio attributed to a specific speaker."""
    
    speaker_id: str
    start_time: float
    end_time: float
    confidence: float
    text: str
    
    @property
    def duration(self) -> float:
        """Duration of the segment in seconds."""
        return self.end_time - self.start_time
    
    @property
    def start_timedelta(self) -> timedelta:
        """Start time as a timedelta object."""
        return timedelta(seconds=self.start_time)
    
    @property
    def end_timedelta(self) -> timedelta:
        """End time as a timedelta object."""
        return timedelta(seconds=self.end_time)


@dataclass
class TranscriptionSegment:
    """Represents a transcription segment with timing information."""
    
    text: str
    start_time: float
    end_time: float
    confidence: float
    language: Optional[str] = None
    
    @property
    def duration(self) -> float:
        """Duration of the segment in seconds."""
        return self.end_time - self.start_time


@dataclass
class DiarizationResult:
    """Complete result of the diarization process."""
    
    audio_file: str
    speakers: List[SpeakerSegment]
    transcription: List[TranscriptionSegment]
    metadata: Dict[str, Any]
    
    @property
    def total_duration(self) -> float:
        """Total duration of the audio file."""
        if not self.transcription:
            return 0.0
        return max(seg.end_time for seg in self.transcription)
    
    @property
    def unique_speakers(self) -> List[str]:
        """List of unique speaker IDs."""
        return list(set(seg.speaker_id for seg in self.speakers))
    
    def get_speaker_segments(self, speaker_id: str) -> List[SpeakerSegment]:
        """Get all segments for a specific speaker."""
        return [seg for seg in self.speakers if seg.speaker_id == speaker_id]
    
    def get_speaker_text(self, speaker_id: str) -> str:
        """Get all text spoken by a specific speaker."""
        segments = self.get_speaker_segments(speaker_id)
        return " ".join(seg.text for seg in segments)
