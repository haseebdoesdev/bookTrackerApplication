from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class BookSearchForm(FlaskForm):
    query = StringField('Search Books', validators=[DataRequired()])
    submit = SubmitField('Search')

class ManualBookAddForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired(), Length(max=255)])
    authors = StringField('Author(s)', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Book Description', validators=[Optional()])
    published_date = StringField('Published Date', validators=[Optional(), Length(max=20)])
    categories = StringField('Categories (comma separated)', validators=[Optional(), Length(max=255)])
    page_count = IntegerField('Number of Pages', validators=[Optional(), NumberRange(min=1)])
    avg_rating = FloatField('Average Rating (0-5)', validators=[Optional(), NumberRange(min=0, max=5)])
    cover_image = StringField('Cover Image URL', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Add Book')

class ReadingProgressForm(FlaskForm):
    status = SelectField('Reading Status', 
                        choices=[
                            ('want_to_read', 'Want to Read'),
                            ('reading', 'Currently Reading'),
                            ('finished', 'Finished Reading')
                        ],
                        validators=[DataRequired()])
    progress = IntegerField('Progress', validators=[Optional(), NumberRange(min=0, max=100)])
    progress_type = SelectField('Progress Type',
                              choices=[
                                  ('percentage', 'Percentage'),
                                  ('page', 'Page Number')
                              ], 
                              validators=[Optional()])
    submit = SubmitField('Update Progress')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    review_text = TextAreaField('Your Review (Markdown supported)', validators=[Optional()])
    submit = SubmitField('Submit Review') 