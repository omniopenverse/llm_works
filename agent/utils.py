


import os
import dspy
from typing import Optional, Literal
from dotenv import load_dotenv

load_dotenv()  # Loads .env variables

class ModelSelector:
    MODELS_MAPPING = {
        "microsoft": "phi4:latest",
        "google": "gemma3:12b",
        "alibaba": "qwen3:14b",
        "gpt": "gpt-4o",
    }
    
    def __init__(
        self,
        service_provider: Literal['azure', 'ollama', 'openai'] = 'ollama',
        model_name: Optional[str] = None):

        """Initialize classifier with invoice data and model configuration."""
        self.service_provider = service_provider.lower()
        self.model_name = model_name          
        if self.service_provider == 'ollama':
            self.free_model = self._resolve_model_naming(model_name)
        elif self.service_provider in ['azure', 'openai']:
            self.paid_model = self._resolve_model_naming(model_name)
    
    def _resolve_model_naming(self, model_input: Optional[str]) -> str:
        """Resolve ollama model name from alias or direct input."""

        if model_input is None:

            return ValueError("Model name has to be provided for a specific service provider.")
        
        return self.MODELS_MAPPING.get(model_input.lower(), model_input)


    def model_selection(self):

        """Configure the language model based on service provider."""
        
        if self.service_provider == 'azure':
            lm = dspy.LM(
                f'azure/{self.paid_model}',
                api_key=os.getenv("AZURE_API_KEY"),
                api_base=os.getenv("AZURE_ENDPOINT"),
                api_version=os.getenv("AZURE_API_VERSION"))
        elif self.service_provider == 'ollama':
            lm = dspy.LM(
                f'ollama_chat/{self.free_model}',
                api_base='http://localhost:11434',
                api_key='')
        elif self.service_provider == 'openai':
            lm = dspy.LM(
                f'openai/{self.paid_model}',
                api_key=os.getenv("OPENAI_API_KEY"),
                cache=False)
        else:
            raise ValueError(f"Unsupported service provider: {self.service_provider}")
        
        dspy.configure(lm=lm)
    
