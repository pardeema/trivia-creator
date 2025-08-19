from app import create_app, db
from app.models import User, Round, Game, Question, GameRound

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Round': Round,
        'Game': Game,
        'Question': Question,
        'GameRound': GameRound
    }

if __name__ == '__main__':
    app.run(debug=True)
