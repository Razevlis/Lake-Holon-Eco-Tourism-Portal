from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ActivityForm(FlaskForm):
    name = StringField('Activity Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('hiking', 'Hiking'),
        ('camping', 'Camping'),
        ('wildlife', 'Wildlife Viewing'),
        ('water_sports', 'Water Sports'),
        ('cultural', 'Cultural Tours'),
        ('photography', 'Photography Tours')
    ], validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard')
    ], validators=[DataRequired()])
    duration_hours = FloatField('Duration (Hours)', validators=[DataRequired(), NumberRange(min=0.5)])
    max_participants = IntegerField('Max Participants', validators=[DataRequired(), NumberRange(min=1)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField('Image URL', validators=[Length(max=200)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Activity')

class GuideForm(FlaskForm):
    name = StringField('Guide Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    specialization = StringField('Specialization', validators=[DataRequired(), Length(max=100)])
    experience_years = IntegerField('Experience Years', validators=[DataRequired(), NumberRange(min=0)])
    bio = TextAreaField('Bio')
    image_url = StringField('Image URL', validators=[Length(max=200)])
    is_available = BooleanField('Available')
    submit = SubmitField('Save Guide')

class TrailForm(FlaskForm):
    name = StringField('Trail Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    difficulty = SelectField('Difficulty', choices=[
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard')
    ], validators=[DataRequired()])
    length_km = FloatField('Length (km)', validators=[DataRequired(), NumberRange(min=0.1)])
    estimated_duration = FloatField('Estimated Duration (hours)', validators=[DataRequired(), NumberRange(min=0.5)])
    elevation_gain = FloatField('Elevation Gain (m)', validators=[NumberRange(min=0)])
    trail_type = SelectField('Trail Type', choices=[
        ('loop', 'Loop'),
        ('out-and-back', 'Out and Back'),
        ('point-to-point', 'Point to Point')
    ])
    start_point = StringField('Start Point', validators=[Length(max=200)])
    end_point = StringField('End Point', validators=[Length(max=200)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Trail')

class AccommodationForm(FlaskForm):
    name = StringField('Accommodation Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    type = SelectField('Type', choices=[
        ('hotel', 'Hotel'),
        ('camping', 'Camping'),
        ('lodge', 'Lodge'),
        ('guesthouse', 'Guest House')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    price_per_night = FloatField('Price per Night', validators=[DataRequired(), NumberRange(min=0)])
    max_occupancy = IntegerField('Max Occupancy', validators=[DataRequired(), NumberRange(min=1)])
    amenities = TextAreaField('Amenities (comma-separated)')
    image_url = StringField('Image URL', validators=[Length(max=200)])
    is_available = BooleanField('Available')
    submit = SubmitField('Save Accommodation')
