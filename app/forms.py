from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, DateField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired()])
    answer_text = TextAreaField('Answer', validators=[DataRequired()])
    points = IntegerField('Points', validators=[Optional(), NumberRange(min=1, max=10)], default=1)

class RoundForm(FlaskForm):
    title = StringField('Round Title', validators=[DataRequired(), Length(max=200)])
    round_label = StringField('Round Label', validators=[DataRequired(), Length(max=50)])
    attachment = FileField('Attachment', validators=[
        FileAllowed(['jpg', 'png', 'gif', 'pdf', 'zip'], 'Images, PDFs, and ZIP files only!')
    ])
    submit = SubmitField('Create Round')

class GameForm(FlaskForm):
    name = StringField('Game Name', validators=[DataRequired(), Length(max=200)])
    game_date = DateField('Game Date', validators=[DataRequired()])
    submit = SubmitField('Create Game')

class RoundSelectionForm(FlaskForm):
    round_id = SelectField('Select Round', coerce=int, validators=[DataRequired()])
    round_order = IntegerField('Order', validators=[DataRequired(), NumberRange(min=1, max=10)], default=1)
    submit = SubmitField('Add Round')
