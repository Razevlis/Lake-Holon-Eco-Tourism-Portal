from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import datetime

class BookingForm(FlaskForm):
    activity_id = SelectField('Activity', coerce=int, validators=[DataRequired()])
    guide_id = SelectField('Guide', coerce=int, validators=[DataRequired()])
    booking_date = DateTimeField('Booking Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    number_of_participants = IntegerField('Number of Participants', validators=[
        DataRequired(), NumberRange(min=1, max=20)
    ])
    special_requests = TextAreaField('Special Requests', validators=[Length(max=500)])
    submit = SubmitField('Book Now')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', coerce=int, choices=[
        (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), 
        (4, '4 Stars'), (5, '5 Stars')
    ], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit Review')
