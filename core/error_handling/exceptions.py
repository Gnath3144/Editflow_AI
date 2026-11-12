"""
Exception Hierarchy for Editflow AI
"""

class EditflowError(Exception):
    """Base exception for all Editflow AI errors."""
    pass

class ConfigurationError(EditflowError):
    """Raised when configuration is missing or invalid."""
    pass

class ProviderNotConfiguredError(EditflowError):
    """Raised when external cloud API keys are absent."""
    pass

class MediaNotFoundError(EditflowError):
    """Raised when video or audio asset is missing."""
    pass

class AudioProcessingError(EditflowError):
    """Raised when audio mastering or time-stretching fails."""
    pass

class TranslationError(EditflowError):
    """Raised when text translation or code shielding fails."""
    pass

class PublishingError(EditflowError):
    """Raised when YouTube metadata or track publishing fails."""
    pass
