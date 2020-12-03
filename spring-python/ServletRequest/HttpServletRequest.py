from .ServletRequest import ServletRequest
from .HttpServletMapping import HttpServletMapping


class HttpServletRequest(ServletRequest):
    BASIC_AUTH = "BASIC"

    FORM_AUTH = "FORM"

    CLIENT_CERT_AUTH = "CLIENT_CERT"

    DIGEST_AUTH = "DIGEST"

    def __init__(self):
        pass

    def get_auth_type(self):
        pass

    def get_cookies(self):
        pass

    def get_date_header(self, name: str):
        pass

    def get_header(self, name: str):
        pass

    def get_headers(self, name: str):
        pass

    def get_header_names(self):
        pass

    def get_int_header(self, name: str):
        pass

    def get_method(self):
        pass

    def get_path_info(self):
        pass

    def get_path_translated(self):
        pass

    def new_push_builder(self):
        pass

    def get_context_path(self):
        pass

    def get_remote_user(self):
        pass

    def is_user_in_role(self, role: str):
        pass

    def get_requested_session_id(self):
        pass

    def get_request_uri(self):
        pass

    def get_request_url(self):
        pass

    def get_servlet_path(self):
        pass

    def get_session(self):
        pass

    def get_session(self, create: bool):
        pass

    def change_session_id(self):
        pass

    def is_requested_session_id_valid(self):
        pass