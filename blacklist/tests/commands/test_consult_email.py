import unittest

from faker import Faker

from src.app import app
from src.commands.email_banned import EmailBanned
from src.database import db
from src.models.blacklist import Blacklist

faker = Faker()


class TestConsultEmail(unittest.TestCase):
    record = {
        'id': faker.uuid4(),
        'email': faker.email(),
        'reason': faker.text(),
        'client_id': faker.uuid4(),
        'ip_address': faker.ipv4()
    }

    def setUp(self):
        with app.app_context():
            record = Blacklist(
                id=self.record['id'],
                email=self.record['email'],
                reason=self.record['reason'],
                client_id=self.record['client_id'],
                ip_address=self.record['ip_address']
            )
            db.session.add(record)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.query(Blacklist).where(Blacklist.email == self.record['email']).delete()
            db.session.commit()

    def test_email_found(self):
        with app.app_context():
            command = EmailBanned(self.record['email'])
            result = command.execute()
            self.assertEqual(result, {"email_found": True, "reason": self.record['reason']})

    def test_email_not_found(self, ):
        with app.app_context():
            command = EmailBanned('test@example.com')
            result = command.execute()
            self.assertEqual(result, {"email_found": False, "reason": ""})
