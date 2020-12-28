from springframework.web.servlet import View
from springframework.utils.mock.inst import HttpStatus

class ModelAndView():

    _view = None
    _model = None
    _status = None
    _cleared = False

    def __init__(self, view=None, model: dict=None, status: HttpStatus=None):
        self._view = view
        self._model = model
        self._status = status
        self._cleared = False

    def 