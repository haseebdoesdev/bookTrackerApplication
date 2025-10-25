from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import Book, ReadingProgress, Challenge

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    if current_user.is_authenticated:
        # Get books the user is currently reading
        reading_entries = ReadingProgress.query.filter_by(
            user_id=current_user.id, 
            status='reading'
        ).order_by(ReadingProgress.last_updated.desc()).limit(3).all()
        
        # Get reading challenges
        active_challenges = Challenge.query.filter_by(
            user_id=current_user.id,
            completed=False
        ).order_by(Challenge.end_date.asc()).limit(1).all()
        
        # Get data for display
        current_books = []
        for entry in reading_entries:
            book = Book.query.get(entry.book_id)
            current_books.append({
                'book': book,
                'progress': entry.progress,
                'progress_type': entry.progress_type
            })
            
        challenge_data = []
        for challenge in active_challenges:
            progress = challenge.get_progress()
            challenge_data.append({
                'challenge': challenge,
                'progress': progress
            })
        
        # Get reading stats
        stats = current_user.get_reading_stats()
        
        return render_template('main/home.html', 
                              title='Home', 
                              current_books=current_books,
                              challenge_data=challenge_data,
                              stats=stats)
    else:
        return render_template('main/welcome.html', title='Welcome to BookTracker')

@main_bp.route('/about')
def about():
    return render_template('main/about.html', title='About') 