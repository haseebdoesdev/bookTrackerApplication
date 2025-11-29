from datetime import datetime
import markdown
import bleach
from app import db

# Allowed HTML tags for markdown output sanitization
ALLOWED_TAGS = [
    'p', 'br', 'b', 'i', 'em', 'strong', 'ul', 'ol', 'li', 
    'a', 'code', 'pre', 'blockquote', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
}

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review_text = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"Review(Book ID: {self.book_id}, Rating: {self.rating})"
    
    def get_formatted_review(self):
        """Convert Markdown to HTML for display with XSS protection"""
        if not self.review_text:
            return ""
        # Convert markdown to HTML
        html = markdown.markdown(self.review_text)
        # Sanitize HTML to prevent XSS attacks
        cleaned = bleach.clean(
            html, 
            tags=ALLOWED_TAGS, 
            attributes=ALLOWED_ATTRIBUTES, 
            strip=True
        )
        return cleaned 