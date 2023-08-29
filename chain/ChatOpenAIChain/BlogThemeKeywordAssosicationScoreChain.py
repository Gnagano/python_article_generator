import json
from .ChatOpenAIChain import ChatOpenAIChain
from ..config.constant import Constant as c

class BlogThemeKeywordAssosicationScoreChain (ChatOpenAIChain):
  TEMPLATE_NAME = c.PROMPT_TEMPLATE_KEYS['blogThemeKeywordAssociationScore']

  def __init__(self, version, model="gpt-3.5-turbo"):
    super().__init__(version=version, model=model)

  def get_response(self, **kwargs):
    # validation for required parameters
    for key in ['problem', 'solution','keywords']:
      if (key) not in kwargs:
        raise ValueError(f'{key} is required')

    jsonStr = self.chain(inputs=kwargs)['text']
    print(jsonStr)
    jsonObj = json.loads(jsonStr)
    return jsonObj
    