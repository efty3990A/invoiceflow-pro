"""InvoiceFlow Pro demo API: Flask + SQLite, session-based role checks."""
import os, sqlite3, secrets
from functools import wraps
from pathlib import Path
from flask import Flask, request, jsonify, session, send_from_directory, abort
from werkzeug.security import check_password_hash

ROOT = Path(__file__).resolve().parents[1]
DB = Path(os.getenv('DATABASE_PATH', ROOT / 'database' / 'invoiceflow.sqlite3'))
app = Flask(__name__, static_folder=str(ROOT), static_url_path='')
app.secret_key = os.getenv('SECRET_KEY', 'dev-only-change-me')
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=os.getenv('COOKIE_SECURE','0')=='1')

def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB); con.row_factory = sqlite3.Row; con.execute('PRAGMA foreign_keys=ON'); return con

def user_required(role=None):
    def deco(fn):
        @wraps(fn)
        def wrapped(*a, **kw):
            if not session.get('user_id'): return jsonify(error='Authentication required'), 401
            if role and session.get('role') != role: return jsonify(error='Insufficient role'), 403
            return fn(*a, **kw)
        return wrapped
    return deco

@app.get('/')
def home(): return send_from_directory(ROOT, 'index.html')
@app.get('/<path:path>')
def static_files(path):
    target = (ROOT / path).resolve()
    if ROOT.resolve() not in target.parents and target != ROOT.resolve(): abort(404)
    if target.is_file(): return send_from_directory(ROOT, path)
    abort(404)

@app.post('/api/login')
def login():
    data=request.get_json(silent=True) or {}; username=data.get('username',''); password=data.get('password','')
    with connect() as db: row=db.execute('SELECT id,username,password_hash,role FROM users WHERE username=? AND active=1',(username,)).fetchone()
    if not row or not check_password_hash(row['password_hash'],password): return jsonify(error='Invalid demo credentials'), 401
    session.clear(); session['user_id']=row['id']; session['username']=row['username']; session['role']=row['role']
    return jsonify(username=row['username'], role=row['role'])

@app.post('/api/logout')
@user_required()
def logout(): session.clear(); return jsonify(ok=True)

@app.get('/api/me')
@user_required()
def me(): return jsonify(username=session['username'], role=session['role'])

@app.get('/api/invoices')
@user_required()
def invoices():
    with connect() as db: rows=db.execute('SELECT id, invoice_number, client_name, total, currency, status, created_at FROM invoices WHERE owner_id=? ORDER BY id DESC',(session['user_id'],)).fetchall()
    return jsonify([dict(r) for r in rows])

@app.post('/api/invoices')
@user_required()
def create_invoice():
    d=request.get_json(silent=True) or {}; required=('invoice_number','client_name','total','currency')
    if any(k not in d for k in required): return jsonify(error='Missing required fields'), 400
    try: total=float(d['total'])
    except (TypeError,ValueError): return jsonify(error='Invalid total'),400
    if total < 0: return jsonify(error='Total cannot be negative'),400
    with connect() as db:
        cur=db.execute('INSERT INTO invoices(owner_id,invoice_number,client_name,total,currency,status,payload) VALUES(?,?,?,?,?,?,?)',(session['user_id'],str(d['invoice_number'])[:80],str(d['client_name'])[:160],total,str(d['currency'])[:8],str(d.get('status','Unpaid'))[:20],__import__('json').dumps(d)))
        return jsonify(id=cur.lastrowid),201

@app.put('/api/invoices/<int:invoice_id>')
@user_required()
def update_invoice(invoice_id):
    d=request.get_json(silent=True) or {}
    with connect() as db:
        row=db.execute('SELECT id FROM invoices WHERE id=? AND owner_id=?',(invoice_id,session['user_id'])).fetchone()
        if not row: return jsonify(error='Invoice not found'),404
        fields={'invoice_number':str(d.get('invoice_number',''))[:80],'client_name':str(d.get('client_name',''))[:160],'total':d.get('total',0),'currency':str(d.get('currency','BDT'))[:8],'status':str(d.get('status','Unpaid'))[:20]}
        try: fields['total']=float(fields['total'])
        except (TypeError,ValueError): return jsonify(error='Invalid total'),400
        db.execute('UPDATE invoices SET invoice_number=?,client_name=?,total=?,currency=?,status=?,payload=? WHERE id=? AND owner_id=?',(*fields.values(),__import__('json').dumps(d),invoice_id,session['user_id']))
    return jsonify(ok=True)

@app.delete('/api/invoices/<int:invoice_id>')
@user_required()
def delete_invoice(invoice_id):
    with connect() as db: cur=db.execute('DELETE FROM invoices WHERE id=? AND owner_id=?',(invoice_id,session['user_id']))
    if not cur.rowcount: return jsonify(error='Invoice not found'),404
    return jsonify(ok=True)

@app.get('/api/admin/users')
@user_required('admin')
def admin_users():
    with connect() as db: rows=db.execute('SELECT id,username,role,active FROM users ORDER BY id').fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')))
