from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Round, Game

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    """Homepage - accessible to everyone"""
    return render_template('index.html', title='Trivia Creator')

@bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - requires authentication"""
    # Get user's recent rounds and games
    recent_rounds = Round.query.filter_by(created_by=current_user.id).order_by(Round.created_at.desc()).limit(5).all()
    recent_games = Game.query.filter_by(created_by=current_user.id).order_by(Game.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         title='Dashboard',
                         recent_rounds=recent_rounds,
                         recent_games=recent_games)
