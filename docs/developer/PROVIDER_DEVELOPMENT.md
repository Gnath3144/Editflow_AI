# Developing External Provider Adapters

This guide explains how to develop, test, and register new external service adapters (such as third-party Translation APIs or Text-to-Speech engines) within **Codealytica Editflow AI**.

---

## 1. Provider Contract Architecture

All external integrations must inherit from abstract base classes located in `automation/multilingual/providers/`:
- `TranslationProviderContract`
- `TTSProviderContract`

---

## 2. Implementing a Translation Provider

```python
from typing import List, Optional
from automation.multilingual.providers.translation_contract import TranslationProviderContract

class CustomTranslationProvider(TranslationProviderContract):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def translate_text(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        """
        Translates text string from source to target language.
        MUST preserve XML tags like <token_0> ... </token_0>.
        """
        # Call provider API
        return translated_text

    def is_available(self) -> bool:
        """Checks API reachability without incurring cost."""
        return bool(self.api_key)
```

---

## 3. Mandatory Provider Testing

Every provider implementation must include a dedicated test file validating:
1. XML shielding tag preservation (tokens like `<token_4>` must not be translated or removed).
2. Proper timeout and error handling when the remote API returns 429 (Rate Limit) or 500 (Internal Server Error).
3. Graceful fallback when credentials are not configured in `.env`.
