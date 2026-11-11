import sqlite3, os
from pathlib import Path
from werkzeug.security import generate_password_hash
root=Path(__file__).resolve().parents[1]; dbpath=Path(os.getenv('DATABASE_PATH',root/'database'/'invoiceflow.sqlite3'))
dbpath.parent.mkdir(parents=True,exist_ok=True)
con=sqlite3.connect(dbpath)
con.executescript((root/'database'/'schema.sql').read_text())
for username,password,role in [('admin-demo','AdminDemo!2026','admin'),('user-demo','UserDemo!2026','user')]:
 con.execute('INSERT OR IGNORE INTO users(username,password_hash,role) VALUES(?,?,?)',(username,generate_password_hash(password),role))
con.commit(); con.close(); print(f'Demo database ready: {dbpath}')
