from app import app, db
from app.models import User, Member, Addition, Subtraction, Singly, Doubly

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Member': Member, 'Addition': Addition, 'Subtraction': Subtraction, 'Singly': Singly, 'Doubly': Doubly}