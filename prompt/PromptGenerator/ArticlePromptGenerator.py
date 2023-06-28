from .PromptGenerator import PromptGenerator
              
class ArticlePromptGenerator (PromptGenerator):
  TEMPLATE_NAME = 'article01'

  def generate_prompt(self, **kwargs):
    print("hello")
