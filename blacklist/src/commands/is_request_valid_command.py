from ..errors.errors import InvalidAppIdFormatRegistrationRequestError, InvalidAppIdRegistrationRequestError, InvalidEmailRegistrationRequestError
from ..utils.common import isUUID

class IsRequesValidCommand:
    def __init__(self, request):
        self.request = request

    def execute(self):
        if (self.request.get_json().get("email") is None):
            raise InvalidEmailRegistrationRequestError
        
        if (self.request.get_json().get("app_uuid") is None):
            raise InvalidAppIdRegistrationRequestError
        
        if (isUUID(self.request.get_json().get("app_uuid")) == False):
            raise InvalidAppIdFormatRegistrationRequestError