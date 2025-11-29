from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, NumberRange, Optional, Length, ValidationError
from datetime import datetime, timedelta

class CreateChallengeForm(FlaskForm):
    title = StringField('Challenge Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    goal = IntegerField('Books Goal', validators=[DataRequired(), NumberRange(min=1)])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Challenge')
    
    def validate_end_date(self, end_date):
        if end_date.data <= datetime.now().date():
            raise ValidationError('End date must be in the future.')
            
class UpdateChallengeForm(FlaskForm):
    title = StringField('Challenge Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    goal = IntegerField('Books Goal', validators=[DataRequired(), NumberRange(min=1)])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Update Challenge') 