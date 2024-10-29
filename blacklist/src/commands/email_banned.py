from src.commands.base_command import BaseCommannd
from src.utils.blacklist_utils import get_blacklist_by_email


class EmailBanned(BaseCommannd):
    def __init__(self, email):
        self.email = email

    def execute(self):
        record = get_blacklist_by_email(self.email)
        if record is None:
            return {"email_found": False, "reason": ""}
        return {"email_found": True, "reason": record.reason}
