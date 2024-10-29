from ..models.blacklist import Blacklist
from ..errors.errors import EmailIsAlreadyRegisteredError

class IsEmailBanneredCommand:
    def __init__(self, email):
        self.email = email

    def execute(self):
        is_email_banner = Blacklist.query.filter(Blacklist.email == self.email).first()

        if (is_email_banner is not None):
            raise EmailIsAlreadyRegisteredError
        