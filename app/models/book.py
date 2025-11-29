from datetime import datetime
from app import db
from markupsafe import Markup
import bleach

# Allowed HTML tags for sanitization
ALLOWED_TAGS = ['p', 'br', 'b', 'i', 'em', 'strong', 'ul', 'ol', 'li', 'span']
ALLOWED_ATTRIBUTES = {}

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    avg_rating = db.Column(db.Float, nullable=True)
    cover_image = db.Column(db.Text, nullable=True)
    published_date = db.Column(db.String(20), nullable=True)
    categories = db.Column(db.String(255), nullable=True)
    page_count = db.Column(db.Integer, nullable=True)
    google_books_id = db.Column(db.String(50), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reading_progress = db.relationship('ReadingProgress', backref='book', lazy=True)
    reviews = db.relationship('Review', backref='book', lazy=True)
    
    def __repr__(self):
        return f"Book('{self.title}', '{self.authors}')"
        
    def get_avg_user_rating(self):
        """Calculate the average rating from user reviews"""
        reviews = Review.query.filter_by(book_id=self.id).all()
        if not reviews:
            return 0
        
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / len(reviews), 1)
    
    def get_formatted_description(self):
        """Safely render HTML content from book description with XSS protection"""
        if not self.description:
            return ""
        # Sanitize HTML to prevent XSS attacks
        cleaned = bleach.clean(
            self.description, 
            tags=ALLOWED_TAGS, 
            attributes=ALLOWED_ATTRIBUTES, 
            strip=True
        )
        return Markup(cleaned)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'description': self.description,
            'avg_rating': self.avg_rating,
            'cover_image': self.cover_image,
            'published_date': self.published_date,
            'categories': self.categories,
            'page_count': self.page_count
        } 