import unittest
from src.app import app
import os
from faker import Faker

fake = Faker()
Faker.seed(1000000)

STATIC_TOKEN = os.environ.get('STATIC_TOKEN')

def mock_task_client():
    class TaskMock:
        def create_task(self):
            return None

    return TaskMock()

class TestRegisterEmailFailsWhenAppIdIsMissing(unittest.TestCase):
    def setUp(self):
        self.headers = {"Authorization": f"Bearer {STATIC_TOKEN}"}
        self.user = dict()
        self.user["email"] = fake.ascii_email()
        self.user["blocked_reason"] = fake.text()

    def test_should_return_400_when_appid_is_missing(self, *args):
        with app.test_client() as test_client:
            response = test_client.post(
                f"/blacklists",
                json=self.user,
                content_type="application/json",
                headers=self.headers,
            )
        assert response.status_code == 400
