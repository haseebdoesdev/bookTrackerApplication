import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if not os.environ.get('SQLALCHEMY_DATABASE_URI'):
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/booktracker.db'

try:
    from app import create_app
    app = create_app()
except Exception as e:
    print(f"[STARTUP ERROR] {e}", flush=True)
    traceback.print_exc()
    raise
