from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    rounds = db.relationship('Round', backref='author', lazy='dynamic')
    games = db.relationship('Game', backref='creator', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    round_label = db.Column(db.String(50), nullable=False)  # e.g., "1", "2", "Music", "Visual"
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attachment_path = db.Column(db.String(500))  # Path to uploaded file
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    questions = db.relationship('Question', backref='round', lazy='dynamic', cascade='all, delete-orphan')
    game_rounds = db.relationship('GameRound', backref='round', lazy='dynamic')
    
    def get_usage_count(self):
        """Get the number of games this round has been used in"""
        return self.game_rounds.count()
    
    def is_new(self):
        """Check if this round has never been used in a game"""
        return self.get_usage_count() == 0
    
    def __repr__(self):
        return f'<Round {self.title}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    question_number = db.Column(db.Integer, nullable=False)  # Order within the round
    points = db.Column(db.Integer, default=1)  # Points for this question
    
    def __repr__(self):
        return f'<Question {self.question_number}: {self.question_text[:50]}...>'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    game_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    game_rounds = db.relationship('GameRound', backref='game', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_rounds(self):
        """Get rounds ordered by round_order"""
        return self.game_rounds.order_by(GameRound.round_order).all()
    
    def get_round_labels(self):
        """Get list of round labels present in this game"""
        return [gr.round.round_label for gr in self.get_rounds()]
    
    def get_missing_round_labels(self, expected_labels=None):
        """Get list of missing round labels"""
        if expected_labels is None:
            expected_labels = ['1', '2', '3', '4', '5', '6']
        present_labels = set(self.get_round_labels())
        return [label for label in expected_labels if label not in present_labels]
    
    def __repr__(self):
        return f'<Game {self.name}>'

class GameRound(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    round_id = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)
    round_order = db.Column(db.Integer, nullable=False)  # Order within the game
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GameRound {self.game_id}:{self.round_id} (order {self.round_order})>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
