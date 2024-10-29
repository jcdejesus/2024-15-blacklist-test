from commands.base_command import BaseCommannd
from models.blacklist import db, Blacklist
from datetime import datetime

class RegisterEmail(BaseCommannd):
  def __init__(self, email, app_uuid, blocked_reason, ip_address):
    self.email = email
    self.app_uuid = app_uuid
    self.blocked_reason = blocked_reason
    self.ip_address = ip_address
  
  def execute(self):
        registered_email = Blacklist(email=self.email, client_id=self.app_uuid,reason=self.blocked_reason, ip_address=self.ip_address, created_at=datetime.utcnow())
        db.session.add(registered_email)
        db.session.commit()

        return True