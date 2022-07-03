from flask_wtf import FlaskForm
from wtforms import DateField, StringField
from wtforms.fields import SubmitField, RadioField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, InputRequired


class NewGameForm(FlaskForm):
    """
    Form for creating a new request.
    """
    name = StringField("Name", validators=[DataRequired()])
    buy_in = IntegerField("Buy-In", validators=[NumberRange(min=0, message="Buy-In should be greater than 0.")])
    members = SelectMultipleField("Members", coerce=int, validators=[InputRequired()])
    submit = SubmitField('Submit')