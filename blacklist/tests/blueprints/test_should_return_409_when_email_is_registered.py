import unittest
from src.app import app
from src.database import db
from faker import Faker
from src.models.blacklist import Blacklist
import os

fake = Faker()
Faker.seed(1000000)

STATIC_TOKEN = os.environ.get('STATIC_TOKEN')

def mock_task_client():
    class TaskMock:
        def create_task(self):
            return None

    return TaskMock()

class TestRegisterEmailFailsWhenEmailIsAlreadyRegistered(unittest.TestCase):
    def setUp(self):
        self.headers = {"Authorization": f"Bearer {STATIC_TOKEN}"}
        self.user = dict()
        self.user["email"] = fake.ascii_email()
        self.user["app_uuid"] = fake.uuid4()
        self.user["blocked_reason"] = fake.text()
        with app.app_context():
            db.create_all()

    def teardown_method(self, args):
        with app.app_context():
            db.session.query(Blacklist).where(Blacklist.email == self.user.get('email')).delete()
            db.session.commit()

    def test_should_return_409_when_email_is_already_registered(self, *args):
        with app.test_client() as test_client:
            with app.app_context():
                record = Blacklist(
                    email=self.user.get("email"),
                    client_id=self.user.get("app_uuid"),
                    reason=self.user.get("blocked_reason"),
                    ip_address=""
                )
                db.session.add(record)
                db.session.commit()
                response = test_client.post(
                    f"/blacklists",
                    json=self.user,
                    content_type="application/json",
                    headers=self.headers,
                )
        assert response.status_code == 409
