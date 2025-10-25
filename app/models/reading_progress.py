from datetime import datetime
from app import db

class ReadingProgress(db.Model):
    __tablename__ = 'reading_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='want_to_read')  # want_to_read, reading, finished
    progress = db.Column(db.Integer, nullable=True, default=0)  # percentage or page number
    progress_type = db.Column(db.String(10), nullable=True, default='percentage')  # percentage or page
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"ReadingProgress(Book ID: {self.book_id}, Status: {self.status}, Progress: {self.progress})"
    
    def update_progress(self, progress, progress_type=None):
        self.progress = progress
        if progress_type:
            self.progress_type = progress_type
        
        # Update status if needed
        if self.progress == 100 and self.progress_type == 'percentage':
            self.status = 'finished'
            self.end_date = datetime.utcnow()
        elif self.status == 'want_to_read' and progress > 0:
            self.status = 'reading'
            if not self.start_date:
                self.start_date = datetime.utcnow()
                
        self.last_updated = datetime.utcnow()
        
    def update_status(self, status):
        old_status = self.status
        self.status = status
        
        # Set appropriate dates
        if status == 'reading' and (old_status == 'want_to_read' or not self.start_date):
            self.start_date = datetime.utcnow()
        elif status == 'finished' and not self.end_date:
            self.end_date = datetime.utcnow()
            if self.progress_type == 'percentage':
                self.progress = 100
            
        self.last_updated = datetime.utcnow() 