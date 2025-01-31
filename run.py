from app import app, db
from app.blueprints.auth.models import User
from app.blueprints.inventory.models import Program

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Program': Program}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
# from app import create_app, db
# from app.blueprints.auth.models import User
# from app.blueprints.inventory.models import Program
# from flask_migrate import Migrate

# app = create_app()
# migrate = Migrate(app, db)

# @app.shell_context_processor
# def make_context():
#     return {'db': db, 'User': User, 'Program': Program}

# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)
