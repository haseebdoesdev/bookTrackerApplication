from datetime import datetime
from app import db

class Challenge(db.Model):
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal = db.Column(db.Integer, nullable=False)  # Number of books to read
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with books
    completed_books = db.relationship('ChallengeBook', backref='challenge', lazy=True)
    
    def __repr__(self):
        return f"Challenge(Goal: {self.goal} books, End Date: {self.end_date})"
    
    def get_progress(self):
        """Return the progress as a percentage"""
        completed = len(self.completed_books)
        return {
            'completed': completed,
            'total': self.goal,
            'percentage': int((completed / self.goal) * 100) if self.goal > 0 else 0
        }
    
    def add_book(self, book_id):
        """Add a book to the challenge's completed books"""
        # Check if book is already added
        existing = ChallengeBook.query.filter_by(challenge_id=self.id, book_id=book_id).first()
        if existing:
            return False
            
        challenge_book = ChallengeBook(challenge_id=self.id, book_id=book_id)
        db.session.add(challenge_book)
        
        # Check if challenge is completed
        if len(self.completed_books) + 1 >= self.goal:
            self.completed = True
            
        return True
        
    def remove_book(self, book_id):
        """Remove a book from the challenge's completed books"""
        challenge_book = ChallengeBook.query.filter_by(challenge_id=self.id, book_id=book_id).first()
        if challenge_book:
            db.session.delete(challenge_book)
            self.completed = False
            return True
        return False

class ChallengeBook(db.Model):
    __tablename__ = 'challenge_books'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"ChallengeBook(Challenge ID: {self.challenge_id}, Book ID: {self.book_id})" 