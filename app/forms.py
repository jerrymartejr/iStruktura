from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class AdditionForm(FlaskForm):
    member_name = StringField('Member Name', validators=[DataRequired()])
    addend1 = IntegerField('Addend1', validators=[DataRequired()])
    addend2 = IntegerField('Addend2', validators=[DataRequired()])
    submit = SubmitField('Add')
    save = SubmitField('Save')


class SubtractionForm(FlaskForm):
    member_name = StringField('Member Name', validators=[DataRequired()])
    minuend = IntegerField('Minuend', validators=[DataRequired()])
    subtrahend = IntegerField('Subtrahend', validators=[DataRequired()])
    submit = SubmitField('Subtract')
    save = SubmitField('Save')


class SinglyForm(FlaskForm):
    member_name = StringField('Member Name', validators=[DataRequired()])
    b = DecimalField('b(mm)', places=2)
    h = DecimalField('h(mm)', places=2)
    cc = DecimalField(Markup('c<sub>c</sub>(mm)'), places=2)
    dbm = DecimalField('db(mm)', places=2)
    dbv = DecimalField(Markup('db<sub>v</sub>(mm)'), places=2)
    fc = DecimalField('fc(MPa)', places=2)
    fy = DecimalField('fy(MPa)', places=2)
    fyv = DecimalField(Markup('fy<sub>v</sub>(MPa)'), places=2)
    k = DecimalField('k', places=2)
    Lc = DecimalField(Markup('L<sub>c</sub>(m)'), places=2)
    λ = DecimalField('λ', places=2)
    Mus = DecimalField(Markup('Mu<sub>s</sub>(kNm)'), places=2)
    Mum = DecimalField(Markup('Mu<sub>m</sub>(kNm)'), places=2)
    Vu = DecimalField('Vu(kN)', places=2)
    Pu = DecimalField('Pu(kN)', places=2)
    Vdl = DecimalField(Markup('V<sub>DL</sub>(kN)'), places=2)
    Vll = DecimalField(Markup('V<sub>LL</sub>(kN)'), places=2)
    submit = SubmitField('Design')
    save = SubmitField('Save')


class DoublyForm(FlaskForm):
    member_name = StringField('Member Name', validators=[DataRequired()])
    b = DecimalField('b(mm)', places=2)
    h = DecimalField('h(mm)', places=2)
    cc = DecimalField(Markup('c<sub>c</sub>(mm)'), places=2)
    dbm = DecimalField('db(mm)', places=2)
    dbv = DecimalField(Markup('db<sub>v</sub>(mm)'), places=2)
    fc = DecimalField('fc(MPa)', places=2)
    fy = DecimalField('fy(MPa)', places=2)
    k = DecimalField('k', places=2)
    Lc = DecimalField(Markup('L<sub>c</sub>(m)'), places=2)
    Mu = DecimalField(Markup('Mu(kNm)'), places=2)
    submit = SubmitField('Design')
    save = SubmitField('Save')

class ReportForm(FlaskForm):
    hidden = HiddenField('Hidden')
    submit = SubmitField('View')

class DeleteForm(FlaskForm):
    hidden = HiddenField('Hidden')
    submit = SubmitField('Delete')

class DetailedReportForm(FlaskForm):
    hidden = HiddenField('Hidden')
    submit = SubmitField('View Detailed Report')