"""Validates translation syntax, code preservation, and completion."""
from typing import Dict, Any, List, Optional
from .glossary_manager import GlossaryManager

class TranslationValidator:
    def __init__(self, glossary_manager: Optional[GlossaryManager] = None):
        self.glossary = glossary_manager or GlossaryManager()

    def validate_translation(self, original_text: str, translated_text: str) -> Dict[str, Any]:
        missing_glossary = self.glossary.validate_preservation(original_text, translated_text)
        has_unresolved_shields = "[[SHIELD_" in translated_text
        is_empty = len(translated_text.strip()) == 0

        is_valid = (len(missing_glossary) == 0) and (not has_unresolved_shields) and (not is_empty)
        return {
            "is_valid": is_valid,
            "missing_glossary_terms": missing_glossary,
            "has_unresolved_shields": has_unresolved_shields,
            "is_empty": is_empty
        }
