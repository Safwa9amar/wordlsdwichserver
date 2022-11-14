from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField,TextAreaField,SelectField, URLField, DateField
from wtforms.validators import DataRequired , Length

class RegForm(FlaskForm):
    class Meta:
     csrf = False
    header = StringField('Header', validators=[DataRequired(),Length(min=2)] )
    tag = SelectField('Tag', validators=[DataRequired()] , choices=('Designs', 'Web'))
    Resume = TextAreaField('Resume', validators=[DataRequired(),Length(min=2)] )
    date = DateField('Posted Date', default=datetime.today)
    en_notion_id = StringField('English Notion id', validators=[DataRequired(),Length(min=2)] )
    ar_notion_id = StringField('Arabic Notion id' )
    ar_darija_notion_id = StringField('Darija Notion id' )
    img = URLField('Image url', validators=[DataRequired()] )
    submit = SubmitField('Save Data')