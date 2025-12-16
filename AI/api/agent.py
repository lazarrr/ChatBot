import os
from typing import Optional
from openai import OpenAI


class GPTAgent:
    """An agent that communicates with OpenAI's GPT model.

    The agent will pick a model in the following order:
    1. `model` argument passed to the constructor
    2. `OPENAI_MODEL` environment variable
    3. default to a GPT-5 series model: `gpt-5-mini`
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the GPT Agent.

        Args:
            api_key: OpenAI API key. If None, will use OPENAI_API_KEY environment variable
            model: The model to use. If None, will read `OPENAI_MODEL` env var or default to `gpt-5-mini`.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)

        self.model = model or "gpt-5-mini"
        self.conversation_history = []
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a message to GPT and get a response.
        
        Args:
            message: The user message to send
            system_prompt: Optional system prompt to override the default behavior
            
        Returns:
            The model's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Prepare messages with optional system prompt
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.extend(self.conversation_history)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
        except Exception as e:
            raise Exception(f"Error communicating with OpenAI: {str(e)}")
    
    def chat_single(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a single message without maintaining conversation history.
        
        Args:
            message: The user message to send
            system_prompt: Optional system prompt to define behavior
            
        Returns:
            The model's response
        """
        print(f"chat_single called with message: {message}, system_prompt: {system_prompt}, model: {self.model}")

        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": message
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error communicating with OpenAI: {str(e)}")
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> list:
        """Get the conversation history."""
        return self.conversation_history
    
    def set_model(self, model: str):
        """Set a different model for the agent."""
        self.model = model
