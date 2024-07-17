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

@inventory.route('/all-items')
def all_items():
    title = 'All items'
    items = Item.query.all()
    return render_template('all_items.html', title=title, items=items)

@inventory.route('/create-item', methods=['GET', 'POST'])
@login_required
def create_item():
    title = 'Create a recommender template'
    form = ItemForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        cost = form.cost.data
        new_item = Item(title=title, description=description, cost=cost, user_id=current_user.id)
        flash(f"{new_item.title} has been created", 'is-success')
        return redirect(url_for('inventory.index'))
    return render_template('create_item.html', title=title, form=form)

@inventory.route('/my-items')
@login_required
def my_items():
    title = 'My Recommender Templates'
    items = current_user.items.all()
    return render_template('my_items.html', title=title, items=items)

@inventory.route('/search-items', methods=['GET', 'POST'])
def search_items():
    title = 'Search'
    form = SearchForm()
    items = []
    if form.validate_on_submit():
        term = form.search.data
        items = Item.query.filter( (Item.title.ilike(f'%{term}%')) | (Item.description.ilike(f'%{term}%')) ).all()
    return render_template('search_items.html', title=title, items=items, form=form)

@inventory.route('/item/<item_id>')
@login_required
def single_item(item_id):
    item = Item.query.get_or_404(item_id)
    title = item.title
    return render_template('item_detail.html', title=title, item=item)

@inventory.route('/edit-items/<item_id>', methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        flash('You do not have edit access to this item.', 'is-danger')
        return redirect(url_for('inventory.my_items'))
    title = f"Edit {item.title}"
    form = ItemForm()
    if form.validate_on_submit():
        item.update(**form.data)
        flash(f'{item.title} has been updated', 'is-success')
        return redirect(url_for('inventory.my_items'))

    return render_template('item_edit.html', title=title, item=item, form=form)

@inventory.route('/delete-items/<item_id>')
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        flash('You do not have delete access to this item', 'is-danger')
    else:
        item.delete()
        flash(f'{item.title} has been deleted.', 'is-success')
    return redirect(url_for('inventory.my_items'))

@inventory.route('/table-of-items')
@login_required
def table_of_items():
    context = {
        'items': Item.query.all()
    }
    return render_template('table_of_items.html', **context)

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
