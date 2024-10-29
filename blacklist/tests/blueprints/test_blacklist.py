import os
import unittest
from unittest.mock import patch

from flask import Flask

from src.blueprints.blacklist import blacklists_blueprint


class TestBlacklist(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(blacklists_blueprint)
        self.client = self.app.test_client()

    @patch('src.blueprints.blacklist.EmailBanned.execute')
    def test_get_blacklist_valid_token(self, mock_execute):
        mock_execute.return_value = {"success": True, "reason": "Test reason"}
        with patch.dict(os.environ, {"STATIC_TOKEN": "valid_token"}):
            response = self.client.get('/blacklists/test@example.com', headers={"Authorization": "Bearer valid_token"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"success": True, "reason": "Test reason"})

    @patch('src.blueprints.blacklist.EmailBanned.execute')
    def test_get_blacklist_invalid_token(self, mock_execute):
        with patch.dict(os.environ, {"STATIC_TOKEN": "valid_token"}):
            response = self.client.get('/blacklists/test@example.com',
                                       headers={"Authorization": "Bearer invalid_token"})
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json, {"msg": "Unauthorized"})

    @patch('src.blueprints.blacklist.EmailBanned.execute')
    def test_get_blacklist_record_not_found(self, mock_execute):
        mock_execute.return_value = {"success": False, "reason": ""}
        with patch.dict(os.environ, {"STATIC_TOKEN": "valid_token"}):
            response = self.client.get('/blacklists/test@example.com', headers={"Authorization": "Bearer valid_token"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"success": False, "reason": ""})

    @patch('src.blueprints.blacklist.EmailBanned.execute')
    def test_get_blacklist_record_found(self, mock_execute):
        mock_execute.return_value = {"success": True, "reason": "Found reason"}
        with patch.dict(os.environ, {"STATIC_TOKEN": "valid_token"}):
            response = self.client.get('/blacklists/test@example.com', headers={"Authorization": "Bearer valid_token"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"success": True, "reason": "Found reason"})
