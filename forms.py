from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import InputRequired, Email, length


class UserForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired(), length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(), length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), length(max=30)])


class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired(), length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])


class AddFeedback(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
