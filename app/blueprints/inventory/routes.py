from . import inventory
from app import app, db #added this line to fix db not found
from flask import redirect, render_template, url_for, flash, session
from flask_login import login_required, current_user
from .forms import ItemForm, SearchForm, ProgramForm, QuizForm
from .models import Item, QuizResponse, Program

@inventory.route('/')
def index():
    title = 'Home'
    return render_template('index.html', title=title)

@inventory.route('/search-items', methods=['GET', 'POST'])
def search_items():
    title = 'Search'
    form = SearchForm()
    items = []
    if form.validate_on_submit():
        term = form.search.data
        items = Item.query.filter( (Item.title.ilike(f'%{term}%')) | (Item.description.ilike(f'%{term}%')) ).all()
    return render_template('search_items.html', title=title, items=items, form=form)

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
        return redirect(url_for('inventory.results'))  # No need for response_id
    return render_template('quiz.html', form=form)

@inventory.route('/results')
def results():
    response = session.get('quiz_response')
    if response is None:
        return redirect(url_for('inventory.quiz'))  # Redirect to quiz if no response found

    programs = Program.query.filter(
        Program.time_commitment.contains(response['time_commitment']),
        Program.years_experience.contains(response['years_experience']),
        Program.topics_addressed.contains(response['topics_addressed'])
    ).all()
    return render_template('results.html', programs=programs)

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
        flash('Program added successfully!')
        return redirect(url_for('inventory.admin'))
    return render_template('admin.html', form=form)

@inventory.route('/programs', methods=['GET'])
def list_programs():
    programs = Program.query.all()
    return render_template('list_programs.html', programs=programs)

@inventory.route('/program/<int:program_id>', methods=['GET'])
def single_program(program_id):
    program = Program.query.get_or_404(program_id)
    return render_template('single_program.html', program=program)
