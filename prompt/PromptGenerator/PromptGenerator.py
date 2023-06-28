import os
from abc import ABC, abstractmethod

class PromptGenerator (ABC):
  TEMPLATE_NAME = ''
  
  def __init__(self):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir_path = os.path.join(current_dir, '../template')
    template_file_path = os.path.join(template_dir_path, f"{self.TEMPLATE_NAME}.txt")
    with open(template_file_path, 'r') as f:
      self.prompt_template = f.read()

  @abstractmethod
  def generate_prompt(self, **kwargs):
      pass