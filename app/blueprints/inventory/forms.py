from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired

class QuizForm(FlaskForm):
    job_role = SelectField('What is your current role?', choices=[('principal', 'Principal'), ('assistant_principal', 'Assistant Principal'), ('teacher_leader', 'Teacher Leader: teachers, network staff, and school support staff')], validators=[DataRequired()])
    years_experience = SelectField('How long have you been in your current role', choices=[('0-1', '0-1'), ('2-5', '2-5'), ('6+', '6+')], validators=[DataRequired()])
    time_commitment = SelectMultipleField(
    'How much time can you commit to a program?',
    choices=[
        ('2_day_workshop', '2 Day Workshop'),
        ('4_5_90_minute_sessions', '4-5, 90 minute sessions throughout the first or second half of the school year'),
        ('monthly_90_minute_sessions', 'Monthly, 90 minute sessions throughout the school year'),
        ('monthly_120_minute_sessions', 'Monthly, 120 minute sessions throughout the school year'),
        ('1_four_hour_session', '1 four-hour session'),
        ('as_needed', 'As needed')
    ],
    validators=[DataRequired()]
)
    topics_addressed = SelectMultipleField(
        'What topics are you interested in?',
        choices=[
            ('budgeting', 'Budgeting'),
            ('community_collaboration', 'Community Collaboration'),
            ('design_thinking', 'Design Thinking'),
            ('differentiated_instruction', 'Differentiated Instruction'),
            ('emotional_intelligence', 'Emotional Intelligence'),
            ('empathy_collaboration', 'Empathy and Collaboration'),
            ('equitable_grading', 'Equitable Grading Practices'),
            ('feedback_on_programming', 'Feedback on Programming'),
            ('innovative_practices', 'Innovative Practices'),
            ('leadership_practices', 'Leadership Practices'),
            ('leadership_networking', 'Leadership Networking'),
            ('mental_health_support', 'Mental Health Support'),
            ('peer_learning', 'Peer Learning'),
            ('positive_school_culture', 'Positive School Culture'),
            ('school_management', 'School Management and Community Partnerships'),
            ('student_centered_instruction', 'Student-Centered Instructional Approaches'),
            ('student_centered_solutions', 'Student-Centered Solutions'),
            ('student_data', 'Leveraging Student Data and Assessments'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')

class ProgramForm(FlaskForm):
    name = StringField('Program Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    job_role = SelectMultipleField('Who is this program geared towards?', choices=[
        ('principal', 'Principal'),
        ('assistant_principal', 'Assistant Principal'),
        ('teacher_leader', 'Teacher Leader: teachers, network staff, and school support staff')
    ], validators=[DataRequired()])
    years_experience = SelectMultipleField('Targeted years of experience', choices=[
        ('0-1', '0-1'),
        ('2-5', '2-5'),
        ('6+', '6+')
    ], validators=[DataRequired()])
    time_commitment = SelectField('Time Commitment', choices=[
        ('2_day_workshop', '2 Day Workshop'),
        ('4_5_90_minute_sessions', '4-5, 90 minute sessions throughout the first or second half of the school year'),
        ('monthly_90_minute_sessions', 'Monthly, 90 minute sessions throughout the school year'),
        ('monthly_120_minute_sessions', 'Monthly, 120 minute sessions throughout the school year'),
        ('1_four_hour_session', '1 four-hour session'),
        ('as_needed', 'As needed')
    ], validators=[DataRequired()])
    topics_addressed = SelectMultipleField(
        'Topics Addressed',
        choices=[
            ('budgeting', 'Budgeting'),
            ('community_collaboration', 'Community Collaboration'),
            ('design_thinking', 'Design Thinking'),
            ('differentiated_instruction', 'Differentiated Instruction'),
            ('emotional_intelligence', 'Emotional Intelligence'),
            ('empathy_collaboration', 'Empathy and Collaboration'),
            ('equitable_grading', 'Equitable Grading Practices'),
            ('feedback_on_programming', 'Feedback on Programming'),
            ('innovative_practices', 'Innovative Practices'),
            ('leadership_practices', 'Leadership Practices'),
            ('leadership_networking', 'Leadership Networking'),
            ('mental_health_support', 'Mental Health Support'),
            ('peer_learning', 'Peer Learning'),
            ('positive_school_culture', 'Positive School Culture'),
            ('school_management', 'School Management and Community Partnerships'),
            ('student_centered_instruction', 'Student-Centered Instructional Approaches'),
            ('student_centered_solutions', 'Student-Centered Solutions'),
            ('student_data', 'Leveraging Student Data and Assessments'),
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')