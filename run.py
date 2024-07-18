from app import app, db
from app.blueprints.auth.models import User
from app.blueprints.inventory.models import Program

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Program': Program}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=port)
