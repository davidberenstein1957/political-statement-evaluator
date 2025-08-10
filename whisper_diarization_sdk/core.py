"""
Core WhisperDiarizer class that integrates with the whisper-diarization repository.
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

from .models import DiarizationResult, SpeakerSegment, TranscriptionSegment


class WhisperDiarizer:
    """
    Main class for performing speaker diarization using OpenAI Whisper and NeMo.

    This class provides a clean interface to the whisper-diarization pipeline
    by wrapping the command-line tools from the cloned repository.
    Supports both audio and video files (MP4, AVI, MOV, etc.).
    """

    def __init__(self, whisper_diarization_path: Optional[str] = None):
        """
        Initialize the WhisperDiarizer.

        Args:
            whisper_diarization_path: Path to the cloned whisper-diarization repository.
                                    If None, will look for it in the current directory.
        """
        if whisper_diarization_path is None:
            # Look for the repository in common locations
            current_dir = Path.cwd()
            possible_paths = [
                current_dir / "whisper-diarization",
                current_dir.parent / "whisper-diarization",
                Path(__file__).parent / "whisper-diarization"
            ]

            for path in possible_paths:
                if path.exists() and (path / "diarize.py").exists():
                    whisper_diarization_path = str(path)
                    break
            else:
                raise FileNotFoundError(
                    "Could not find whisper-diarization repository. "
                    "Please specify the path explicitly."
                )

        self.whisper_diarization_path = Path(whisper_diarization_path)
        self._validate_repository()

    def _validate_repository(self) -> None:
        """Validate that the whisper-diarization repository is properly set up."""
        required_files = ["diarize.py", "requirements.txt", "helpers.py"]
        for file in required_files:
            if not (self.whisper_diarization_path / file).exists():
                raise FileNotFoundError(
                    f"Required file {file} not found in {self.whisper_diarization_path}"
                )

    def _is_video_file(self, file_path: str) -> bool:
        """Check if the file is a video file based on extension."""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp'}
        return Path(file_path).suffix.lower() in video_extensions

    def _extract_audio_from_video(self, video_file: str) -> str:
        """
        Extract audio from video file using ffmpeg.

        Args:
            video_file: Path to the video file

        Returns:
            Path to the extracted audio file (WAV format)

        Raises:
            RuntimeError: If ffmpeg is not available or extraction fails
        """
        try:
            # Check if ffmpeg is available
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError(
                "ffmpeg is required for video processing. "
                "Please install ffmpeg: https://ffmpeg.org/download.html"
            )

        # Create temporary file for extracted audio
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio.close()

        try:
            # Extract audio using ffmpeg
            cmd = [
                'ffmpeg', '-i', video_file,
                '-vn',  # No video
                '-acodec', 'pcm_s16le',  # PCM 16-bit
                '-ar', '16000',  # 16kHz sample rate
                '-ac', '1',  # Mono
                '-y',  # Overwrite output file
                temp_audio.name
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return temp_audio.name

        except subprocess.CalledProcessError as e:
            # Clean up temp file on failure
            Path(temp_audio.name).unlink(missing_ok=True)
            raise RuntimeError(f"Failed to extract audio from video: {e.stderr}") from e

    def diarize(
        self,
        audio_file: str,
        whisper_model: str = "medium.en",
        suppress_numerals: bool = True,
        device: str = "auto",
        language: Optional[str] = None,
        batch_size: int = 0,
        output_format: str = "json"
    ) -> DiarizationResult:
        """
        Perform speaker diarization on an audio or video file.

        Args:
            audio_file: Path to the audio or video file to process
            whisper_model: Whisper model to use (default: medium.en)
            suppress_numerals: Whether to suppress numerals in transcription
            device: Device to use (cuda, cpu, or auto)
            language: Language code (if known)
            batch_size: Batch size for processing (0 for non-batched)
            output_format: Output format (json, srt, txt)

        Returns:
            DiarizationResult object containing the diarization results
        """
        # Validate file exists
        if not Path(audio_file).exists():
            raise FileNotFoundError(f"File not found: {audio_file}")

        # Handle video files by extracting audio first
        temp_audio_file = None
        try:
            if self._is_video_file(audio_file):
                print(f"Detected video file: {audio_file}")
                print("Extracting audio for processing...")
                temp_audio_file = self._extract_audio_from_video(audio_file)
                print(f"Audio extracted to: {temp_audio_file}")
                processing_file = temp_audio_file
            else:
                processing_file = audio_file

            # Build command arguments
            cmd = [
                sys.executable,
                str(self.whisper_diarization_path / "diarize.py"),
                "-a", processing_file,
                "--whisper-model", whisper_model,
                "--device", device,
                "--batch-size", str(batch_size)
            ]

            if suppress_numerals:
                cmd.append("--suppress_numerals")

            if language:
                cmd.extend(["--language", language])

            # Run the diarization
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=self.whisper_diarization_path,
                    check=True
                )

                # Parse the output and create DiarizationResult
                return self._parse_output(result.stdout, audio_file)

            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Diarization failed: {e.stderr}"
                ) from e

        finally:
            # Clean up temporary audio file if it was created
            if temp_audio_file and Path(temp_audio_file).exists():
                Path(temp_audio_file).unlink()
                print(f"Cleaned up temporary audio file: {temp_audio_file}")

    def _parse_output(self, output: str, audio_file: str) -> DiarizationResult:
        """
        Parse the output from the diarization script.

        This is a simplified parser - in practice, you might want to modify
        the diarization script to output structured data.
        """
        # For now, create a basic result structure
        # In practice, you'd want to modify the diarization script to output JSON
        metadata = {
            "processing_time": None,
            "whisper_model": None,
            "num_speakers": 0,
            "audio_duration": None
        }

        # Create placeholder segments (you'd parse the actual output here)
        speakers: List[SpeakerSegment] = []
        transcription: List[TranscriptionSegment] = []

        return DiarizationResult(
            audio_file=audio_file,
            speakers=speakers,
            transcription=transcription,
            metadata=metadata
        )

    def get_available_models(self) -> List[str]:
        """Get list of available Whisper models."""
        return [
            "tiny.en", "tiny", "base.en", "base", "small.en", "small",
            "medium.en", "medium", "large-v1", "large-v2", "large-v3"
        ]

    def get_supported_languages(self) -> List[str]:
        """Get list of supported language codes."""
        return [
            "en", "zh", "de", "es", "ru", "ko", "fr", "ja", "pt", "tr",
            "pl", "ca", "nl", "ar", "sv", "it", "id", "hi", "fi", "vi",
            "he", "uk", "el", "ms", "cs", "ro", "da", "hu", "ta", "no",
            "th", "ur", "hr", "bg", "lt", "la", "mi", "ml", "cy", "sk",
            "te", "fa", "lv", "bn", "sr", "az", "sl", "kn", "et", "mk",
            "br", "eu", "is", "hy", "ne", "mn", "bs", "kk", "sq", "sw",
            "gl", "mr", "pa", "si", "km", "sn", "yo", "so", "af", "oc",
            "ka", "be", "tg", "sd", "gu", "am", "yi", "lo", "uz", "fo",
            "ht", "ps", "tk", "nn", "mt", "sa", "lb", "my", "bo", "tl",
            "mg", "as", "tt", "haw", "ln", "ha", "ba", "jw", "su"
        ]

    def get_supported_video_formats(self) -> List[str]:
        """Get list of supported video file extensions."""
        return ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.3gp']

    def is_video_processing_available(self) -> bool:
        """
        Check if video processing is available (ffmpeg installed).

        Returns:
            True if ffmpeg is available, False otherwise
        """
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def get_video_info(self, video_file: str) -> dict:
        """
        Get basic information about a video file using ffmpeg.

        Args:
            video_file: Path to the video file

        Returns:
            Dictionary containing video information (duration, resolution, etc.)

        Raises:
            RuntimeError: If ffmpeg is not available or file doesn't exist
        """
        if not self.is_video_processing_available():
            raise RuntimeError("ffmpeg is required for video processing")

        if not Path(video_file).exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")

        try:
            cmd = [
                'ffmpeg', '-i', video_file,
                '-f', 'null', '-'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            # Parse ffmpeg output for duration and other info
            info: dict = {}

            # Extract duration from stderr (ffmpeg outputs info to stderr)
            duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})', result.stderr)
            if duration_match:
                hours, minutes, seconds, centiseconds = map(int, duration_match.groups())
                info['duration'] = hours * 3600 + minutes * 60 + seconds + centiseconds / 100

            # Extract resolution
            resolution_match = re.search(r'(\d{3,4})x(\d{3,4})', result.stderr)
            if resolution_match:
                info['width'] = int(resolution_match.group(1))
                info['height'] = int(resolution_match.group(2))

            # Extract audio codec
            audio_match = re.search(r'Audio: (\w+)', result.stderr)
            if audio_match:
                info['audio_codec'] = audio_match.group(1)

            # Extract video codec
            video_match = re.search(r'Video: (\w+)', result.stderr)
            if video_match:
                info['video_codec'] = video_match.group(1)

            return info

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get video info: {e.stderr}") from e
