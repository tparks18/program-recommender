from app import app, db
from app.blueprints.auth.models import User
from app.blueprints.inventory.models import Item


@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Item': Item}
