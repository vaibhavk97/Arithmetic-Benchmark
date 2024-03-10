import anthropic
import os 
from .base_provider import Model 
import time

SYSTEM_PROMPT = "You are a calculator. DO NOT use scientific notation, reply with the complete result for any operation. Think step by step and compute your answer, take a deep breath, lets go!"

class AnthropicProvider(Model):
    def __init__(self, name):
      self.client = anthropic.Anthropic(
          api_key=os.environ.get("ANTHROPIC_API_KEY"))
      self.name = name
    
    def predict(self, message):
      response = self.client.messages.create(model=self.name,
                                             max_tokens=1000,
                                             temperature=0.2,
                                             system=SYSTEM_PROMPT,
                                             messages=[{
                                                 "role":
                                                 "user",
                                                 "content":
                                                 f"What is {message} ?"
                                             }])
      time.sleep(3) #to prevent being rate limited.
      return response.content[0].text