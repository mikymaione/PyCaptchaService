from unittest import TestCase
from fastapi.testclient import TestClient
from CaptchaService import app


class Test(TestCase):
    client = TestClient(app)

    def test_welcome(self):
        response = self.client.get("/")

        assert response.status_code == 200
        assert response.json() == {"Hello": "World!"}

    def test_generate_captcha(self):
        response = self.client.get("/generate")

        assert response.status_code == 200

        j = response.json()

        assert "guid" in j
        assert "captcha" in j

    def test_validate_captcha(self):
        answer_json = {
            "answer": "test",
            "guid": "0"
        }

        response_validate = self.client.post("/validate/", json=answer_json)
        assert response_validate.status_code == 200
        assert response_validate.json() == {"Correct": False}
