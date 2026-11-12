import unittest
from automation.multilingual.app.glossary_manager import GlossaryManager

class TestGlossary(unittest.TestCase):
    def setUp(self):
        self.manager = GlossaryManager()

    def test_protected_tokens_loaded(self):
        critical_tokens = [
            "Python", "Java", "SQL", "Generative AI", "Artificial Intelligence",
            "Machine Learning", "Deep Learning", "Large Language Model", "LLM",
            "RAG", "Prompt Engineering", "Tokens", "Embeddings", "Vector Database",
            "Transformers", "Neural Networks", "API", "JSON", "GitHub", "Visual Studio Code",
            "Ollama", "Gemma", "Qwen", "GPU", "CPU", "RAM", "VRAM", "Fine-tuning",
            "Inference", "Model Parameters", "Docker", "LangChain", "LangGraph",
            "Databricks", "Snowflake", "dbt", "Pydantic", "PyTorch", "CUDA", "NVENC"
        ]
        for token in critical_tokens:
            self.assertTrue(self.manager.is_protected_token(token), f"Token {token} not found in protected glossary")

    def test_validate_preservation_detects_missing(self):
        orig = "In this lesson we use Pydantic models with Ollama and RAG."
        trans_ok = "Is sabak mein hum Pydantic models ko Ollama aur RAG ke saath upyog karenge."
        trans_bad = "Is sabak mein hum models ko aur ke saath upyog karenge."
        
        self.assertEqual(len(self.manager.validate_preservation(orig, trans_ok)), 0)
        missing = self.manager.validate_preservation(orig, trans_bad)
        self.assertIn("Pydantic", missing)
        self.assertIn("Ollama", missing)
        self.assertIn("RAG", missing)

if __name__ == "__main__":
    unittest.main()
