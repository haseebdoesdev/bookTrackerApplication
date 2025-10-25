import os
import requests
from flask import Blueprint, render_template, url_for, flash, redirect, request, jsonify
from flask_login import current_user, login_required
from app import db
from app.models import Book, ReadingProgress, Review
from app.forms import BookSearchForm, ManualBookAddForm, ReadingProgressForm, ReviewForm
from fuzzywuzzy import fuzz

books_bp = Blueprint('books', __name__)

def search_google_books(query):
    """Search for books using Google Books API"""
    api_key = os.environ.get('GOOGLE_BOOKS_API_KEY', '')
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=40"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []
    
    data = response.json()
    if 'items' not in data:
        return []
    
    books = []
    for item in data['items']:
        volume_info = item.get('volumeInfo', {})
        
        # Extract book information
        book = {
            'id': item.get('id', ''),
            'title': volume_info.get('title', 'Unknown Title'),
            'authors': volume_info.get('authors', ['Unknown Author']),
            'description': volume_info.get('description', ''),
            'rating': volume_info.get('averageRating', 0),
            'published_date': volume_info.get('publishedDate', ''),
            'categories': volume_info.get('categories', []),
            'page_count': volume_info.get('pageCount', 0),
            'cover_image': None
        }
        
        # Extract cover image if available
        if 'imageLinks' in volume_info:
            cover_url = volume_info['imageLinks'].get('thumbnail')
            # Make sure the cover URL isn't too long
            if cover_url and len(cover_url) > 1000:  # Set a reasonable limit for safety
                # Try to use a smaller image if available
                if 'smallThumbnail' in volume_info['imageLinks']:
                    cover_url = volume_info['imageLinks'].get('smallThumbnail')
            book['cover_image'] = cover_url
            
        # Calculate relevance score using fuzzy matching
        title_score = fuzz.token_set_ratio(query.lower(), book['title'].lower())
        
        # If authors is a list, join them for matching
        if isinstance(book['authors'], list):
            authors_text = ', '.join(book['authors'])
        else:
            authors_text = book['authors']
            
        author_score = fuzz.token_set_ratio(query.lower(), authors_text.lower())
        
        # Consider description if available
        description_score = 0
        if book['description']:
            description_score = fuzz.token_set_ratio(query.lower(), book['description'].lower()) * 0.3  # Lower weight for description
        
        # Calculate weighted relevance score
        book['relevance_score'] = (title_score * 0.6) + (author_score * 0.3) + (description_score * 0.1)
            
        books.append(book)
    
    # Sort books by relevance score (highest first)
    books.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    return books

@books_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = BookSearchForm()
    results = []
    
    if form.validate_on_submit() or request.args.get('query'):
        query = form.query.data if form.validate_on_submit() else request.args.get('query')
        results = search_google_books(query)
    
    return render_template('books/search.html', title='Search Books', form=form, results=results)

@books_bp.route('/add_manual', methods=['GET', 'POST'])
@login_required
def add_manual():
    form = ManualBookAddForm()
    
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            authors=form.authors.data,
            description=form.description.data,
            published_date=form.published_date.data,
            categories=form.categories.data,
            page_count=form.page_count.data,
            avg_rating=form.avg_rating.data,
            cover_image=form.cover_image.data,
            user_id=current_user.id
        )
        
        db.session.add(book)
        db.session.commit()
        
        # Add reading progress record
        progress = ReadingProgress(
            user_id=current_user.id,
            book_id=book.id,
            status='want_to_read'
        )
        
        db.session.add(progress)
        db.session.commit()
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('books.view', book_id=book.id))
    
    return render_template('books/add_manual.html', title='Add Book Manually', form=form)

@books_bp.route('/add_from_api/<string:google_id>')
@login_required
def add_from_api(google_id):
    # Check if book already exists
    existing_book = Book.query.filter_by(google_books_id=google_id, user_id=current_user.id).first()
    if existing_book:
        flash('This book is already in your library!', 'info')
        return redirect(url_for('books.view', book_id=existing_book.id))
    
    # Get book details from API
    api_key = os.environ.get('GOOGLE_BOOKS_API_KEY', '')
    url = f"https://www.googleapis.com/books/v1/volumes/{google_id}?key={api_key}"
    
    response = requests.get(url)
    if response.status_code != 200:
        flash('Error fetching book details.', 'danger')
        return redirect(url_for('books.search'))
    
    data = response.json()
    volume_info = data.get('volumeInfo', {})
    
    # Create book object
    book = Book(
        title=volume_info.get('title', 'Unknown Title'),
        authors=', '.join(volume_info.get('authors', ['Unknown Author'])),
        description=volume_info.get('description', ''),
        avg_rating=volume_info.get('averageRating', 0),
        published_date=volume_info.get('publishedDate', ''),
        categories=', '.join(volume_info.get('categories', [])) if 'categories' in volume_info else '',
        page_count=volume_info.get('pageCount', 0),
        google_books_id=google_id,
        user_id=current_user.id
    )
    
    # Get cover image if available
    if 'imageLinks' in volume_info:
        cover_url = volume_info['imageLinks'].get('thumbnail')
        # Make sure the cover URL isn't too long
        if cover_url and len(cover_url) > 1000:  # Set a reasonable limit for safety
            # Try to use a smaller image if available
            if 'smallThumbnail' in volume_info['imageLinks']:
                cover_url = volume_info['imageLinks'].get('smallThumbnail')
        book.cover_image = cover_url
    
    db.session.add(book)
    db.session.commit()
    
    # Add reading progress record
    progress = ReadingProgress(
        user_id=current_user.id,
        book_id=book.id,
        status='want_to_read'
    )
    
    db.session.add(progress)
    db.session.commit()
    
    flash('Book added to your library!', 'success')
    return redirect(url_for('books.view', book_id=book.id))

@books_bp.route('/library')
@login_required
def library():
    # Get query parameters for filtering
    status_filter = request.args.get('status', 'all')
    category_filter = request.args.get('category', 'all')
    rating_filter = request.args.get('rating', 'all')
    
    # Base query - get reading progress entries for current user
    query = ReadingProgress.query.filter_by(user_id=current_user.id)
    
    # Apply status filter
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Get progress entries
    reading_entries = query.all()
    
    # Collect books and related data
    library_data = []
    for entry in reading_entries:
        book = Book.query.get(entry.book_id)
        
        # Apply category filter
        if category_filter != 'all' and (not book.categories or category_filter not in book.categories):
            continue
            
        # Apply rating filter
        if rating_filter != 'all':
            min_rating = int(rating_filter)
            if book.avg_rating < min_rating:
                continue
        
        library_data.append({
            'book': book,
            'progress': entry
        })
    
    # Get available categories for filter dropdown
    all_books = Book.query.filter_by(user_id=current_user.id).all()
    categories = set()
    for book in all_books:
        if book.categories:
            for category in book.categories.split(','):
                categories.add(category.strip())
    
    return render_template('books/library.html', 
                          title='My Library', 
                          library_data=library_data,
                          categories=sorted(list(categories)),
                          status_filter=status_filter,
                          category_filter=category_filter,
                          rating_filter=rating_filter)

@books_bp.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def view(book_id):
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    progress = ReadingProgress.query.filter_by(book_id=book_id, user_id=current_user.id).first_or_404()
    
    # Progress form
    progress_form = ReadingProgressForm()
    if progress_form.validate_on_submit() and 'update_progress' in request.form:
        progress.update_status(progress_form.status.data)
        if progress_form.progress.data is not None:
            progress.update_progress(progress_form.progress.data, progress_form.progress_type.data)
        
        db.session.commit()
        flash('Reading progress updated!', 'success')
        return redirect(url_for('books.view', book_id=book_id))
    elif request.method == 'GET':
        progress_form.status.data = progress.status
        progress_form.progress.data = progress.progress
        progress_form.progress_type.data = progress.progress_type
    
    # Review form
    review = Review.query.filter_by(book_id=book_id, user_id=current_user.id).first()
    review_form = ReviewForm()
    
    if review_form.validate_on_submit() and 'submit_review' in request.form:
        if review:
            review.rating = review_form.rating.data
            review.review_text = review_form.review_text.data
        else:
            review = Review(
                user_id=current_user.id,
                book_id=book_id,
                rating=review_form.rating.data,
                review_text=review_form.review_text.data
            )
            db.session.add(review)
        
        db.session.commit()
        flash('Your review has been submitted!', 'success')
        return redirect(url_for('books.view', book_id=book_id))
    elif request.method == 'GET' and review:
        review_form.rating.data = review.rating
        review_form.review_text.data = review.review_text
    
    # Get other reviews
    other_reviews = Review.query.filter(
        Review.book_id == book_id,
        Review.user_id != current_user.id
    ).all()
    
    return render_template('books/view.html',
                          title=book.title,
                          book=book,
                          progress=progress,
                          progress_form=progress_form,
                          review=review,
                          review_form=review_form,
                          other_reviews=other_reviews)

@books_bp.route('/book/<int:book_id>/delete', methods=['POST'])
@login_required
def delete(book_id):
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    
    # Delete associated records
    ReadingProgress.query.filter_by(book_id=book_id).delete()
    Review.query.filter_by(book_id=book_id).delete()
    
    db.session.delete(book)
    db.session.commit()
    
    flash('Book has been deleted from your library.', 'success')
    return redirect(url_for('books.library')) 