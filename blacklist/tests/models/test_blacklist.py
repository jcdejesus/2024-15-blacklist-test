from faker import Faker

from src.app import app
from src.database import db
from src.models.blacklist import Blacklist

fake = Faker()


class TestBlacklistModel:
    new_record = None

    def setup_method(self):
        self.new_record = {
            'email': fake.email(),
            'client_id': fake.uuid4(),
            'reason': fake.text(),
            'ip_address': fake.ipv4()
        }
        with app.app_context():
            db.create_all()

    def teardown_method(self):
        with app.app_context():
            db.session.query(Blacklist).where(Blacklist.email == self.new_record['email']).delete()
            db.session.commit()

    def test_blacklist_creation_success(self):
        with app.app_context():
            record = Blacklist(
                email=self.new_record['email'],
                client_id=self.new_record['client_id'],
                reason=self.new_record['reason'],
                ip_address=self.new_record['ip_address']
            )
            db.session.add(record)
            db.session.commit()

            assert record.email == self.new_record['email']
            assert record.client_id == self.new_record['client_id']
            assert record.reason == self.new_record['reason']
            assert record.ip_address == self.new_record['ip_address']
            assert record.id is not None
            assert record.created_at is not None
