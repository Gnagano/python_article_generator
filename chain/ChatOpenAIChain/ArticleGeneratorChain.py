from .ChatOpenAIChain import ChatOpenAIChain
from ..config.constant import Constant as c

class ArticleGeneratorChain (ChatOpenAIChain):
  TEMPLATE_NAME = c.PROMPT_TEMPLATE_KEYS['article01']

  def get_response(self, **kwargs):
    # validation for required parameters
    if 'title' not in kwargs:
      raise ValueError('title is required')

    return self.chain(inputs=kwargs)['text']
