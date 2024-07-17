from . import inventory #is my blueprint registered???
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import ItemForm, SearchForm
from .models import Item

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
    title = 'Create an item'
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