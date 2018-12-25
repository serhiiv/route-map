from app import app, db
from app.models import User, Route, Invoice


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Route': Route, 'Invoice': Invoice}
