from .ChatOpenAIChain import ChatOpenAIChain
from ..config.constant import Constant as c

class ArticleGeneratorChain (ChatOpenAIChain):
  TEMPLATE_NAME = c.PROMPT_TEMPLATE_KEYS['article']

  def __init__(self, version="1.0", model="gpt-3.5-turbo"):
    super().__init__(version=version, model=model)

  def get_response(self, **kwargs):
    # validation for required parameters
    if 'title' not in kwargs:
      raise ValueError('title is required')

    return self.chain(inputs=kwargs)['text']
