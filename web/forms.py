from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField,SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Length,EqualTo
from web.models import User

class CreatePasteForm(FlaskForm):
    title = StringField(validators=[DataRequired(),Length(max=256)])
    text = TextAreaField(render_kw={'rows':15})
    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if not user or username_to_check.data=='guest':
            raise ValidationError(f'User with the username "{username_to_check.data}" does not exist')  

    username = StringField(validators=[DataRequired(),Length(min=4)])
    password = PasswordField(validators=[DataRequired(),Length(min=6)])
    submit = SubmitField(label='Login')

class SignUpForm(FlaskForm):
    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user or username_to_check.data=='guest':
            raise ValidationError(f'User with the username "{username_to_check.data}" aleardy exist')

    username = StringField(validators=[DataRequired(),Length(min=4)])
    password1 = PasswordField(validators=[DataRequired(),Length(min=6)])
    password2 = PasswordField(validators=[EqualTo('password1',message='Passwords do not match')])
    submit = SubmitField(label='Sign Up')