import unittest

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_homepage_renders_personalized_site(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Vivek Kumar", response.data)
        self.assertIn(b"TechWorld", response.data)
        self.assertIn(b"Kubernetes", response.data)

    def test_contact_link_uses_configured_email(self):
        app.config["CONTACT_EMAIL"] = "vivek@example.com"
        try:
            response = self.client.get("/")
        finally:
            app.config["CONTACT_EMAIL"] = ""

        self.assertIn(b"mailto:vivek@example.com", response.data)

    def test_health_and_readiness_probes(self):
        for path, state in (("/healthz", b"healthy"), ("/readyz", b"ready")):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(state, response.data)


if __name__ == "__main__":
    unittest.main()
