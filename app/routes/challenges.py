from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from app.models import Challenge, ChallengeBook, Book, ReadingProgress
from app.forms import CreateChallengeForm, UpdateChallengeForm

challenges_bp = Blueprint('challenges', __name__)

@challenges_bp.route('/challenges')
@login_required
def list_challenges():
    # Get active and completed challenges
    active_challenges = Challenge.query.filter_by(
        user_id=current_user.id,
        completed=False
    ).order_by(Challenge.end_date.asc()).all()
    
    completed_challenges = Challenge.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).order_by(Challenge.end_date.desc()).all()
    
    # Calculate progress for each challenge
    challenges_data = []
    for challenge in active_challenges:
        progress = challenge.get_progress()
        days_left = (challenge.end_date - datetime.utcnow()).days
        challenges_data.append({
            'challenge': challenge,
            'progress': progress,
            'days_left': max(0, days_left)
        })
    
    completed_data = []
    for challenge in completed_challenges:
        progress = challenge.get_progress()
        completed_data.append({
            'challenge': challenge,
            'progress': progress
        })
    
    return render_template('challenges/list.html',
                          title='Reading Challenges',
                          challenges_data=challenges_data,
                          completed_data=completed_data)

@challenges_bp.route('/challenges/create', methods=['GET', 'POST'])
@login_required
def create_challenge():
    form = CreateChallengeForm()
    
    if form.validate_on_submit():
        challenge = Challenge(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            goal=form.goal.data,
            start_date=datetime.utcnow(),
            end_date=form.end_date.data
        )
        
        db.session.add(challenge)
        db.session.commit()
        
        flash('Reading challenge created successfully!', 'success')
        return redirect(url_for('challenges.view', challenge_id=challenge.id))
    
    return render_template('challenges/create.html', title='Create Challenge', form=form)

@challenges_bp.route('/challenges/<int:challenge_id>')
@login_required
def view(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id, user_id=current_user.id).first_or_404()
    progress = challenge.get_progress()
    
    days_total = max(1, (challenge.end_date - challenge.start_date).days)
    days_passed = (datetime.utcnow() - challenge.start_date).days
    days_left = (challenge.end_date - datetime.utcnow()).days
    
    time_progress = min(100, int((days_passed / days_total) * 100))
    
    # Get completed books for this challenge
    completed_books = []
    for challenge_book in challenge.completed_books:
        book = Book.query.get(challenge_book.book_id)
        if book:
            completed_books.append({
                'book': book,
                'date_added': challenge_book.date_added
            })
    
    # Sort books by date added to challenge
    completed_books.sort(key=lambda x: x['date_added'], reverse=True)
    
    # Get candidate books (finished books not in challenge)
    finished_entries = ReadingProgress.query.filter_by(
        user_id=current_user.id,
        status='finished'
    ).all()
    
    candidate_books = []
    challenge_book_ids = [cb.book_id for cb in challenge.completed_books]
    
    for entry in finished_entries:
        if entry.book_id not in challenge_book_ids:
            book = Book.query.get(entry.book_id)
            if book:
                candidate_books.append(book)
    
    return render_template('challenges/view.html',
                          title=f'Challenge: {challenge.title}',
                          challenge=challenge,
                          progress=progress,
                          days_left=max(0, days_left),
                          time_progress=time_progress,
                          completed_books=completed_books,
                          candidate_books=candidate_books)

@challenges_bp.route('/challenges/<int:challenge_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id, user_id=current_user.id).first_or_404()
    
    # Don't allow editing completed challenges
    if challenge.completed:
        flash('Completed challenges cannot be edited.', 'info')
        return redirect(url_for('challenges.view', challenge_id=challenge.id))
    
    form = UpdateChallengeForm()
    
    if form.validate_on_submit():
        challenge.title = form.title.data
        challenge.description = form.description.data
        challenge.goal = form.goal.data
        challenge.end_date = form.end_date.data
        
        db.session.commit()
        
        flash('Challenge updated successfully!', 'success')
        return redirect(url_for('challenges.view', challenge_id=challenge.id))
    elif request.method == 'GET':
        form.title.data = challenge.title
        form.description.data = challenge.description
        form.goal.data = challenge.goal
        form.end_date.data = challenge.end_date
    
    return render_template('challenges/edit.html', title='Edit Challenge', form=form, challenge=challenge)

@challenges_bp.route('/challenges/<int:challenge_id>/delete', methods=['POST'])
@login_required
def delete(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id, user_id=current_user.id).first_or_404()
    
    # Delete challenge books
    ChallengeBook.query.filter_by(challenge_id=challenge.id).delete()
    
    db.session.delete(challenge)
    db.session.commit()
    
    flash('Challenge has been deleted.', 'success')
    return redirect(url_for('challenges.list_challenges'))

@challenges_bp.route('/challenges/<int:challenge_id>/add_book/<int:book_id>', methods=['POST'])
@login_required
def add_book(challenge_id, book_id):
    challenge = Challenge.query.filter_by(id=challenge_id, user_id=current_user.id).first_or_404()
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    
    # Check if book is finished
    progress = ReadingProgress.query.filter_by(book_id=book_id, user_id=current_user.id).first()
    if not progress or progress.status != 'finished':
        flash('Only finished books can be added to a challenge.', 'warning')
        return redirect(url_for('challenges.view', challenge_id=challenge.id))
    
    if challenge.add_book(book_id):
        db.session.commit()
        flash(f'"{book.title}" has been added to your challenge!', 'success')
    else:
        flash('This book is already part of the challenge.', 'info')
    
    return redirect(url_for('challenges.view', challenge_id=challenge.id))

@challenges_bp.route('/challenges/<int:challenge_id>/remove_book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(challenge_id, book_id):
    challenge = Challenge.query.filter_by(id=challenge_id, user_id=current_user.id).first_or_404()
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    
    if challenge.remove_book(book_id):
        db.session.commit()
        flash(f'"{book.title}" has been removed from your challenge.', 'success')
    else:
        flash('This book is not part of the challenge.', 'warning')
    
    return redirect(url_for('challenges.view', challenge_id=challenge.id)) 