from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    status = SelectField(
        'Status',
        choices=[('Active', 'Active'), ('Completed', 'Completed'), ('On Hold', 'On Hold')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Save Project')
