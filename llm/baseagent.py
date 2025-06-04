from anthropic import Anthropic
import os

class BaseClaudeAgent:
    
    def __init__(self, api_key="api_key", model="claude-4-opus-20250514"):
        
        self.model = model
        self.client = Anthropic(api_key=api_key)

    def call(self, content, images = None):
        if images:
            content_block = [{"type": "text", "text": content}]
            content_block += images
        else:
            content_block = content
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": content_block}]
        )
        return response.content[0].text.strip()
