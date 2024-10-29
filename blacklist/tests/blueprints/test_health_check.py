from src.app import app


class TestUsersHealthCheck:
    def test_ping_pong_is_service_alive(self):
        with app.test_client() as test_client:
            response = test_client.get("/blacklists/ping")
        assert response.status_code == 200
        assert response.data == b'pong'
