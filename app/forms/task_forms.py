from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Length(max=1000)])
    project_id = SelectField('Project', coerce=int, validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Completed', 'Completed')],
        validators=[DataRequired()]
    )
    priority = SelectField(
        'Priority',
        choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')],
        validators=[DataRequired()]
    )
    due_date = DateField('Due Date', validators=[Optional()])
    submit = SubmitField('Save Task')
