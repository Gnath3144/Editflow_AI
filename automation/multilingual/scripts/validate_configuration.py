"""
Validates all multilingual JSON configs, language profiles, schemas, and terminology glossary.
Usage:
  python -m automation.multilingual.scripts.validate_configuration
"""

import os
import sys
import json

CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")

EXPECTED_12_LOCALES = [
    "ta-IN", "te-IN", "ml-IN", "hi-IN", "ur-PK", "zh-CN",
    "ja-JP", "ko-KR", "ms-MY", "en-SG", "en-GB", "en-US"
]

def validate_json_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return True, data, "Valid JSON"
    except Exception as e:
        return False, None, str(e)

def main():
    print("[*] Validating Multilingual Configuration Files...")
    all_ok = True
    configs = {}

    for fname in os.listdir(CONFIG_DIR):
        if fname.endswith(".json"):
            p = os.path.join(CONFIG_DIR, fname)
            ok, data, msg = validate_json_file(p)
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {fname}: {msg}")
            if not ok:
                all_ok = False
            else:
                configs[fname] = data

    print("\n[*] Validating JSON Schema Files...")
    for fname in os.listdir(SCHEMA_DIR):
        if fname.endswith(".json"):
            p = os.path.join(SCHEMA_DIR, fname)
            ok, _, msg = validate_json_file(p)
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {fname}: {msg}")
            if not ok:
                all_ok = False

    print("\n[*] Validating 12 Target Language Profiles in languages.json...")
    lang_data = configs.get("languages.json", {})
    locales_found = list(lang_data.keys())

    # Check uniqueness
    if len(locales_found) != len(set(locales_found)):
        print("  [FAIL] Duplicate locales found in languages.json!")
        all_ok = False
    else:
        print("  [PASS] All configured locales are unique.")

    for loc in EXPECTED_12_LOCALES:
        if loc in lang_data:
            prof = lang_data[loc]
            print(f"  [PASS] {loc}: {prof.get('display_name')} ({prof.get('native_name')}) [Dir: {prof.get('text_direction')}]")
        else:
            print(f"  [FAIL] Missing required language profile: {loc}")
            all_ok = False

    print("\n[*] Validating Terminology Glossary...")
    glossary = configs.get("terminology_glossary.json", {})
    tokens = glossary.get("shielded_tokens", [])
    print(f"  [PASS] Shielded Technical Tokens Count: {len(tokens)}")
    for critical_token in ["Python", "Java", "SQL", "LLM", "RAG", "Pydantic", "Docker", "GPU", "CUDA"]:
        if critical_token in tokens:
            print(f"    - Protected: {critical_token}")
        else:
            print(f"    - [FAIL] Missing critical term: {critical_token}")
            all_ok = False

    if all_ok:
        print("\n[+] All configuration and schema validations passed (100% SUCCESS).")
        sys.exit(0)
    else:
        print("\n[-] Validation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
