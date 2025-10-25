from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager, bcrypt
from app.models.reading_progress import ReadingProgress

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True, default='default.jpg')
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    books = db.relationship('Book', backref='owner', lazy=True)
    reading_entries = db.relationship('ReadingProgress', backref='reader', lazy=True)
    challenges = db.relationship('Challenge', backref='participant', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def get_reading_stats(self):
        # Calculate reading statistics
        books_read = ReadingProgress.query.filter(
            ReadingProgress.user_id == self.id,
            (ReadingProgress.status == 'finished') | (ReadingProgress.status == 'read')
        ).count()
        
        books_reading = ReadingProgress.query.filter_by(user_id=self.id, status='reading').count()
        
        books_to_read = ReadingProgress.query.filter(
            ReadingProgress.user_id == self.id,
            (ReadingProgress.status == 'want_to_read') | (ReadingProgress.status == 'to-read')
        ).count()
        
        return {
            'read': books_read,
            'reading': books_reading,
            'to_read': books_to_read,
            'total': books_read + books_reading + books_to_read
        }
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')" 