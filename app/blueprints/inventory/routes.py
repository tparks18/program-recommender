from . import inventory
from app import app, db
from flask import redirect, render_template, url_for, flash, session, request
from flask_login import login_required, current_user
from .forms import ProgramForm, QuizForm
from .models import QuizResponse, Program


@inventory.route('/program/<int:program_id>/edit', methods=['GET', 'POST'])
def edit_program(program_id):
    program = Program.query.get_or_404(program_id)
    form = ProgramForm(obj=program)
    
    if form.validate_on_submit():
        program.name = form.name.data
        program.description = form.description.data
        program.job_role = ', '.join(form.job_role.data)
        program.years_experience = ', '.join(form.years_experience.data)
        program.time_commitment = form.time_commitment.data
        program.topics_addressed = ', '.join(form.topics_addressed.data)
        
        db.session.commit()
        flash(f'{program.name} has been updated', 'is-success')
        return redirect(url_for('inventory.single_program', program_id=program_id))
    
    return render_template('edit_program.html', form=form, program=program)

@inventory.route('/delete-program/<int:program_id>')
@login_required
def delete_program(program_id):
    program = Program.query.get_or_404(program_id)
    program.delete()
    flash(f'{program.name} has been deleted.', 'is-success')
    return redirect(url_for('inventory.list_programs'))

def calculate_match_score(program, form_data):
    # Exclude specific programs based on job role
    if form_data["job_role"] in ["principal", "assistant_principal"] and program.name == "EAC":
        return 0
    
    # Ensure exact match for time commitment
    if program.time_commitment not in form_data["time_commitment"].split(', '):
        return 0

    score = 0
    if form_data["job_role"] in program.job_role:
        score += 1
    if form_data["years_experience"] in program.years_experience:
        score += 1
    if any(topic in program.topics_addressed for topic in form_data["topics_addressed"].split(', ')):
        score += 1
    return score

def get_matching_programs(form_data):
    programs = Program.query.all()
    scored_programs = []
    for program in programs:
        score = calculate_match_score(program, form_data)
        if score > 0:
            scored_programs.append((program, score))
    scored_programs.sort(key=lambda x: x[1], reverse=True)
    return [program for program, score in scored_programs]

@inventory.route('/quiz', methods=['GET', 'POST'])
def quiz():
    form = QuizForm()
    if form.validate_on_submit():
        response = {
            'job_role': form.job_role.data,
            'years_experience': form.years_experience.data,
            'time_commitment': ', '.join(form.time_commitment.data),
            'topics_addressed': ', '.join(form.topics_addressed.data)
        }
        session['quiz_response'] = response
        return redirect(url_for('inventory.results'))
    return render_template('quiz.html', form=form)

@inventory.route('/results')
def results():
    response = session.get('quiz_response')
    if response is None:
        return redirect(url_for('inventory.quiz'))  # Redirect to quiz if no response found

    matching_programs = get_matching_programs(response)
    return render_template('results.html', programs=matching_programs)

@inventory.route('/admin', methods=['GET', 'POST'])
def admin():
    form = ProgramForm()
    if form.validate_on_submit():
        program = Program(
            name=form.name.data,
            description=form.description.data,
            job_role=', '.join(form.job_role.data),
            years_experience=', '.join(form.years_experience.data),
            time_commitment=form.time_commitment.data,
            topics_addressed=', '.join(form.topics_addressed.data)
        )
        db.session.add(program)
        db.session.commit()
        flash(f'{program.name} has been added successfully', 'is-success')
        return redirect(url_for('inventory.admin'))
    return render_template('admin.html', form=form)

@inventory.route('/programs', methods=['GET', 'POST'])
def list_programs():
    search_query = request.args.get('search', '')
    if search_query:
        programs = Program.query.filter(Program.name.ilike(f'%{search_query}%')).all()
    else:
        programs = Program.query.all()
    return render_template('list_programs.html', programs=programs, search_query=search_query)

@inventory.route('/program/<int:program_id>', methods=['GET'])
def single_program(program_id):
    program = Program.query.get_or_404(program_id)
    return render_template('single_program.html', program=program)

