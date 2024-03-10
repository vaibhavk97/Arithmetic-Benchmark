from openai import OpenAI
from .base_provider import Model
import os
import time

SYSTEM_PROMPT = "You are a calculator. DO NOT use scientific notation, reply with the complete result for any operation. Think step by step and compute your answer, take a deep breath, lets go!"

class OpenAIProvider(Model):
    def __init__(self, name):
      self.name = name
      self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def predict(self, message):
      response = self.client.chat.completions.create(
          temperature=0.2,
          messages=[{
              "role": "system",
              "content": SYSTEM_PROMPT
          }, {
              "role": "user",
              "content": f"What is {message} ?"
          }],
          model=self.name,
      )
      time.sleep(1)
      return response.choices[0].message.content
    