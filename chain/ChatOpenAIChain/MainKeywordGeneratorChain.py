import json
from .ChatOpenAIChain import ChatOpenAIChain
from ..config.constant import Constant as c

class MainKeywordGeneratorChain (ChatOpenAIChain):
  TEMPLATE_NAME = c.PROMPT_TEMPLATE_KEYS['mainKeyword01']

  def get_response(self, **kwargs):
    # validation for required parameters
    for key in ['problem', 'solution']:
      if (key) not in kwargs:
        raise ValueError(f'{key} is required')

    jsonStr = self.chain(inputs=kwargs)['text']
    jsonObj = json.loads(jsonStr)
    keywords = [item['keyword'] for item in jsonObj]
    return keywords