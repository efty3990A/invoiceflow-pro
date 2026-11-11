import os
import tempfile
import unittest
from pathlib import Path

TMP = tempfile.TemporaryDirectory()
os.environ["SECRET_KEY"] = "test-secret-key-with-more-than-32-characters"
os.environ["DATABASE_PATH"] = str(Path(TMP.name) / "test.sqlite3")
os.environ["DEMO_ADMIN_PASSWORD"] = "Admin-test-password-2026-unique"
os.environ["DEMO_USER_PASSWORD"] = "User-test-password-2026-unique"
os.environ["COOKIE_SECURE"] = "0"

from database.seed import DB  # initializes schema and test demo accounts
from backend.app import app

class ApiSecurityTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SECRET_KEY=os.environ["SECRET_KEY"])
        self.client = app.test_client()

    def login(self, role):
        response = self.client.post(f"/api/demo-login/{role}")
        self.assertEqual(response.status_code, 200)
        return response.get_json()["csrf_token"]

    def test_health(self):
        self.assertEqual(self.client.get('/healthz').status_code, 200)

    def test_mutations_require_auth(self):
        response = self.client.post('/api/invoices', json={"invoice_number":"A1","client_name":"X","total":1,"currency":"USD"})
        self.assertEqual(response.status_code, 401)

    def test_mutations_require_csrf(self):
        self.login('user')
        response = self.client.post('/api/invoices', json={"invoice_number":"A1","client_name":"X","total":1,"currency":"USD"})
        self.assertEqual(response.status_code, 403)

    def test_user_cannot_access_admin_route(self):
        self.login('user')
        self.assertEqual(self.client.get('/api/admin/users').status_code, 403)

    def test_invoice_owner_scope_and_csrf(self):
        token = self.login('user')
        headers = {"X-CSRF-Token": token}
        created = self.client.post('/api/invoices', json={"invoice_number":"A1","client_name":"Client","total":12,"currency":"USD"}, headers=headers)
        self.assertEqual(created.status_code, 201)
        self.assertEqual(len(self.client.get('/api/invoices').get_json()), 1)
        self.client.post('/api/logout', headers=headers)
        self.login('admin')
        self.assertEqual(self.client.get('/api/invoices').get_json(), [])

    def test_demo_role_validation(self):
        self.assertEqual(self.client.post('/api/demo-login/root').status_code, 404)

if __name__ == '__main__':
    unittest.main()
