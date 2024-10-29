import unittest
import os
from src.app import app
from src.utils.constants import EMAIL_REGISTERED
from faker import Faker
from src.database import db
from src.models.blacklist import Blacklist

fake = Faker()
Faker.seed(1000000)

STATIC_TOKEN = os.environ.get('STATIC_TOKEN')

def mock_task_client():
    class TaskMock:
        def create_task(self):
            return None

    return TaskMock()

class TestRegisterEmail(unittest.TestCase):
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

    def test_should_return_200_when_email_gets_registered(self, *args):
        with app.test_client() as test_client:
            response = test_client.post(
                f"/blacklists",
                json=self.user,
                content_type="application/json",
                headers=self.headers,
            )
            body = response.json
        assert response.status_code == 201
        assert body["msg"] == EMAIL_REGISTERED
