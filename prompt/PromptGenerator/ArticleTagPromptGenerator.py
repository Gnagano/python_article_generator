from .PromptGenerator import PromptGenerator
from ..config.constant import Constant as c

class ArticleTagPromptGenerator (PromptGenerator):
  TEMPLATE_NAME = c.PROMPT_TEMPLATE_KEYS['articleTag01']

  def generate_prompt(self, **kwargs):
    # validation for required parameters
    if 'title' not in kwargs:
      raise ValueError('title is required')

    return self.prompt_template.format(title=kwargs['title'])
