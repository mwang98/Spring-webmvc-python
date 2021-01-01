from abc import ABC, abstractclassmethod
from springframework.web.testfixture.servlet import MockHttpServletRequest


class CorUtils():

    def is_pre_flight_request(self, httpServletRequest: MockHttpServletRequest) -> bool:
        return False