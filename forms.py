from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class IssueForm(FlaskForm):
    tablet = SelectField('Номер планшета', validators=[DataRequired()], coerce=int)
    leader = StringField('ФИО руководителя', validators=[DataRequired()])
    brigade_number = StringField('Номер бригады', validators=[DataRequired()])
    issue_date = DateField('Дата выдачи', format='%Y-%m-%d', default=None, validators=[DataRequired()])
    submit = SubmitField('Добавить')
