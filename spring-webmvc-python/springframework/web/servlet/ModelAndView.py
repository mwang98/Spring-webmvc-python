from springframework.http import HttpStatus
from springframework.ui import ModelMap
from springFramework.util import CoolectionUtils


class ModelAndView():
    
    def __init__(self, view=None, model=None, status=None):
        self._view = view
        self._model = model
        self._status = status
        self._cleared = False
        
    def 