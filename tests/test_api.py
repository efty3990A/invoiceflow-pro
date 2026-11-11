import os, tempfile, unittest
from pathlib import Path
from werkzeug.security import generate_password_hash
os.environ['SECRET_KEY']='test-secret'
from backend import app as module

class ApiTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); module.DB=Path(self.tmp.name)/'test.sqlite3'
  with module.connect() as db:
   db.executescript((Path(__file__).resolve().parents[1]/'database/schema.sql').read_text())
   db.execute('INSERT INTO users(username,password_hash,role) VALUES(?,?,?)',('admin-demo',generate_password_hash('AdminDemo!2026'),'admin'))
   db.execute('INSERT INTO users(username,password_hash,role) VALUES(?,?,?)',('user-demo',generate_password_hash('UserDemo!2026'),'user'))
  self.client=module.app.test_client()
 def tearDown(self): self.tmp.cleanup()
 def test_auth_required_for_mutation(self): self.assertEqual(self.client.post('/api/invoices',json={}).status_code,401)
 def test_user_can_create_and_delete_own_invoice(self):
  self.client.post('/api/login',json={'username':'user-demo','password':'UserDemo!2026'})
  r=self.client.post('/api/invoices',json={'invoice_number':'INV-1','client_name':'Demo','total':10,'currency':'USD'})
  self.assertEqual(r.status_code,201); iid=r.json['id']; self.assertEqual(self.client.delete(f'/api/invoices/{iid}').status_code,200)
 def test_user_cannot_access_admin_route(self):
  self.client.post('/api/login',json={'username':'user-demo','password':'UserDemo!2026'})
  self.assertEqual(self.client.get('/api/admin/users').status_code,403)
 def test_admin_can_access_admin_route(self):
  self.client.post('/api/login',json={'username':'admin-demo','password':'AdminDemo!2026'})
  self.assertEqual(self.client.get('/api/admin/users').status_code,200)
if __name__=='__main__': unittest.main()
