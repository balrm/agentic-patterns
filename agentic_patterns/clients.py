"""
LLM client implementations for popular providers.
"""

import asyncio
from typing import Any, Dict, Optional
from .base import LLMClient


class MockLLMClient(LLMClient):
    """Mock LLM client for testing and development."""
    
    def __init__(self, responses: Optional[Dict[str, str]] = None):
        self.responses = responses or {}
        self.call_count = 0
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate a mock response."""
        self.call_count += 1
        
        # Return predefined response if available
        if prompt in self.responses:
            return self.responses[prompt]
        
        # Default mock responses based on prompt content
        if "think step by step" in prompt.lower():
            return "Let me think about this step by step:\n1. First, I need to understand the problem\n2. Then, I'll analyze the key components\n3. Finally, I'll provide a solution"
        elif "evaluate" in prompt.lower():
            return "Score: 8/10. This response is well-structured and addresses the main points effectively."
        elif "reflection" in prompt.lower() or "what went wrong" in prompt.lower():
            return "The response could be more specific and include concrete examples."
        elif "debate" in prompt.lower() or "perspective" in prompt.lower():
            return "From my perspective, this approach has merit but should be balanced with alternative considerations."
        else:
            return f"Mock response #{self.call_count}: {prompt[:50]}..."
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate mock cost."""
        return len(prompt + response) / 1000.0


class OpenAIClient(LLMClient):
    """OpenAI API client implementation."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", **kwargs):
        try:
            import openai
            self.client = openai.AsyncOpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI client requires 'openai' package. Install with: pip install openai")
        
        self.model = model
        self.config = kwargs
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using OpenAI API."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **{**self.config, **kwargs}
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}") from e
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate cost based on token count."""
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model(self.model)
            prompt_tokens = len(encoding.encode(prompt))
            response_tokens = len(encoding.encode(response))
            
            # Rough cost estimation (varies by model)
            if "gpt-4" in self.model:
                return (prompt_tokens * 0.03 + response_tokens * 0.06) / 1000
            else:
                return (prompt_tokens * 0.0015 + response_tokens * 0.002) / 1000
        except ImportError:
            # Fallback to character-based estimation
            return len(prompt + response) / 1000.0


class AnthropicClient(LLMClient):
    """Anthropic Claude API client implementation."""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229", **kwargs):
        try:
            import anthropic
            self.client = anthropic.AsyncAnthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic client requires 'anthropic' package. Install with: pip install anthropic")
        
        self.model = model
        self.config = kwargs
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Anthropic API."""
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
                **{**self.config, **kwargs}
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {str(e)}") from e
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate cost based on token count."""
        try:
            import tiktoken
            # Claude uses cl100k_base encoding
            encoding = tiktoken.get_encoding("cl100k_base")
            prompt_tokens = len(encoding.encode(prompt))
            response_tokens = len(encoding.encode(response))
            
            # Rough cost estimation for Claude models
            if "claude-3-opus" in self.model:
                return (prompt_tokens * 0.015 + response_tokens * 0.075) / 1000
            elif "claude-3-sonnet" in self.model:
                return (prompt_tokens * 0.003 + response_tokens * 0.015) / 1000
            else:
                return (prompt_tokens * 0.0008 + response_tokens * 0.0024) / 1000
        except ImportError:
            # Fallback to character-based estimation
            return len(prompt + response) / 1000.0


class GoogleGeminiClient(LLMClient):
    """Google Gemini API client implementation."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash", **kwargs):
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model)
        except ImportError:
            raise ImportError("Google Gemini client requires 'google-generativeai' package. Install with: pip install google-generativeai")
        
        self.model_name = model
        self.config = kwargs
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Google Gemini API."""
        try:
            # Note: google-generativeai doesn't have async support yet, so we run in thread
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(prompt, **{**self.config, **kwargs})
            )
            
            # Handle different response formats
            if hasattr(response, 'text'):
                return response.text
            elif hasattr(response, 'parts') and response.parts:
                return response.parts[0].text
            elif isinstance(response, str):
                return response
            else:
                return str(response)
        except Exception as e:
            raise RuntimeError(f"Google Gemini API call failed: {str(e)}") from e
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate cost based on character count (Gemini pricing)."""
        # Gemini pricing is per character
        total_chars = len(prompt + response)
        return total_chars * 0.00025 / 1000  # $0.00025 per 1K characters


class CohereClient(LLMClient):
    """Cohere API client implementation."""
    
    def __init__(self, api_key: str, model: str = "command", **kwargs):
        try:
            import cohere
            self.client = cohere.AsyncClient(api_key=api_key)
        except ImportError:
            raise ImportError("Cohere client requires 'cohere' package. Install with: pip install cohere")
        
        self.model = model
        self.config = kwargs
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Cohere API."""
        try:
            response = await self.client.generate(
                model=self.model,
                prompt=prompt,
                **{**self.config, **kwargs}
            )
            return response.generations[0].text
        except Exception as e:
            raise RuntimeError(f"Cohere API call failed: {str(e)}") from e
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate cost based on token count."""
        # Cohere pricing varies by model, using rough estimates
        total_chars = len(prompt + response)
        return total_chars * 0.00015 / 1000  # Rough estimate


class HuggingFaceClient(LLMClient):
    """Hugging Face Inference API client implementation."""
    
    def __init__(self, api_key: str, model: str = "meta-llama/Llama-2-7b-chat-hf", **kwargs):
        try:
            import requests
            self.requests = requests
        except ImportError:
            raise ImportError("Hugging Face client requires 'requests' package. Install with: pip install requests")
        
        self.api_key = api_key
        self.model = model
        self.config = kwargs
        self.base_url = "https://api-inference.huggingface.co/models"
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Hugging Face Inference API."""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "inputs": prompt,
                **{**self.config, **kwargs}
            }
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.requests.post(f"{self.base_url}/{self.model}", headers=headers, json=payload)
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"API request failed with status {response.status_code}")
            
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            elif isinstance(result, dict):
                return result.get("generated_text", "")
            else:
                return str(result)
        except Exception as e:
            raise RuntimeError(f"Hugging Face API call failed: {str(e)}") from e
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate cost - Hugging Face pricing varies by model."""
        # Free tier available, paid pricing varies
        return 0.0  # Free tier


class AzureOpenAIClient(LLMClient):
    """Azure OpenAI API client implementation."""
    
    def __init__(self, api_key: str, endpoint: str, model: str = "gpt-35-turbo", **kwargs):
        try:
            import openai
            self.client = openai.AsyncAzureOpenAI(
                api_key=api_key,
                azure_endpoint=endpoint,
                api_version=kwargs.get("api_version", "2024-02-15-preview")
            )
        except ImportError:
            raise ImportError("Azure OpenAI client requires 'openai' package. Install with: pip install openai")
        
        self.model = model
        self.config = kwargs
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using Azure OpenAI API."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **{**self.config, **kwargs}
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Azure OpenAI API call failed: {str(e)}") from e
    
    def estimate_cost(self, prompt: str, response: str) -> float:
        """Estimate cost based on token count."""
        try:
            import tiktoken
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Use standard encoding
            prompt_tokens = len(encoding.encode(prompt))
            response_tokens = len(encoding.encode(response))
            
            # Azure pricing is similar to OpenAI but may vary
            return (prompt_tokens * 0.0015 + response_tokens * 0.002) / 1000
        except ImportError:
            return len(prompt + response) / 1000.0


def create_client(provider: str, **kwargs) -> LLMClient:
    """
    Factory function to create LLM clients.
    
    Args:
        provider: Provider name ('openai', 'anthropic', 'google', 'cohere', 'huggingface', 'azure', 'mock')
        **kwargs: Provider-specific configuration
        
    Returns:
        LLMClient instance
    """
    provider = provider.lower()
    
    if provider == "openai":
        if "api_key" not in kwargs:
            raise ValueError("OpenAI client requires 'api_key' parameter")
        return OpenAIClient(**kwargs)
    
    elif provider == "anthropic":
        if "api_key" not in kwargs:
            raise ValueError("Anthropic client requires 'api_key' parameter")
        return AnthropicClient(**kwargs)
    
    elif provider == "google" or provider == "gemini":
        if "api_key" not in kwargs:
            raise ValueError("Google Gemini client requires 'api_key' parameter")
        return GoogleGeminiClient(**kwargs)
    
    elif provider == "cohere":
        if "api_key" not in kwargs:
            raise ValueError("Cohere client requires 'api_key' parameter")
        return CohereClient(**kwargs)
    
    elif provider == "huggingface" or provider == "hf":
        if "api_key" not in kwargs:
            raise ValueError("Hugging Face client requires 'api_key' parameter")
        return HuggingFaceClient(**kwargs)
    
    elif provider == "azure":
        if "api_key" not in kwargs:
            raise ValueError("Azure OpenAI client requires 'api_key' parameter")
        if "endpoint" not in kwargs:
            raise ValueError("Azure OpenAI client requires 'endpoint' parameter")
        return AzureOpenAIClient(**kwargs)
    
    elif provider == "mock":
        return MockLLMClient(**kwargs)
    
    else:
        available = "openai, anthropic, google/gemini, cohere, huggingface/hf, azure, mock"
        raise ValueError(f"Unknown provider '{provider}'. Available: {available}") 