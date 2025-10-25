from flask import Blueprint, render_template
from flask_login import current_user, login_required
from datetime import datetime
from app.models import ReadingProgress, Book, Review, Challenge

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/stats')
@login_required
def stats():
    # Get reading stats
    stats = current_user.get_reading_stats()
    
    # Get recently read books
    finished_entries = ReadingProgress.query.filter_by(
        user_id=current_user.id,
        status='finished'
    ).order_by(ReadingProgress.end_date.desc()).limit(5).all()
    
    recent_books = []
    for entry in finished_entries:
        book = Book.query.get(entry.book_id)
        if book:
            recent_books.append({
                'book': book,
                'date_finished': entry.end_date
            })
    
    # Get reading activity (books finished per month)
    year = datetime.now().year
    monthly_stats = []
    
    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        count = ReadingProgress.query.filter(
            ReadingProgress.user_id == current_user.id,
            ReadingProgress.status == 'finished',
            ReadingProgress.end_date >= start_date,
            ReadingProgress.end_date < end_date
        ).count()
        
        monthly_stats.append({
            'month': start_date.strftime('%b'),
            'count': count
        })
    
    # Get top rated books
    top_rated = Book.query.join(Review, Book.id == Review.book_id).filter(
        Book.user_id == current_user.id,
        Review.user_id == current_user.id
    ).order_by(Review.rating.desc()).limit(3).all()
    
    # Get active challenges
    active_challenges = Challenge.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(Challenge.end_date.asc()).all()
    
    challenges_data = []
    for challenge in active_challenges:
        progress = challenge.get_progress()
        days_left = (challenge.end_date - datetime.utcnow()).days
        challenges_data.append({
            'challenge': challenge,
            'progress': progress,
            'days_left': max(0, days_left)
        })
    
    return render_template('profile/stats.html',
                          title='Reading Stats',
                          stats=stats,
                          recent_books=recent_books,
                          monthly_stats=monthly_stats,
                          top_rated=top_rated,
                          challenges_data=challenges_data) 