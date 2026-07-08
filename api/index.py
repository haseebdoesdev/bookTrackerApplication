import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if not os.environ.get('SQLALCHEMY_DATABASE_URI'):
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/booktracker.db'

from app import create_app

app = create_app()
