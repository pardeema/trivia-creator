from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Game, Round, GameRound
from app.forms import GameForm, RoundSelectionForm

bp = Blueprint('games', __name__)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = GameForm()
    if form.validate_on_submit():
        # Generate default name if not provided
        name = form.name.data
        if not name:
            name = form.game_date.data.strftime('%A, %B %d %Y')
        
        game = Game(
            name=name,
            game_date=form.game_date.data,
            created_by=current_user.id
        )
        db.session.add(game)
        db.session.commit()
        
        flash(f'Game "{name}" created successfully!')
        return redirect(url_for('games.edit', game_id=game.id))
    
    return render_template('games/create.html', title='Create Game', form=form)

@bp.route('/<int:game_id>')
def view(game_id):
    game = Game.query.get_or_404(game_id)
    game_rounds = game.get_rounds()
    return render_template('games/view.html', 
                         title=game.name,
                         game=game,
                         game_rounds=game_rounds)

@bp.route('/<int:game_id>/edit')
@login_required
def edit(game_id):
    game = Game.query.get_or_404(game_id)
    
    # Check if user owns this game
    if game.created_by != current_user.id:
        flash('You can only edit your own games.')
        return redirect(url_for('games.view', game_id=game_id))
    
    game_rounds = game.get_rounds()
    available_rounds = Round.query.filter_by(is_active=True).order_by(Round.title).all()
    
    return render_template('games/edit.html', 
                         title=f'Edit Game - {game.name}',
                         game=game,
                         game_rounds=game_rounds,
                         available_rounds=available_rounds)

@bp.route('/<int:game_id>/add-round', methods=['POST'])
@login_required
def add_round(game_id):
    game = Game.query.get_or_404(game_id)
    
    # Check if user owns this game
    if game.created_by != current_user.id:
        flash('You can only edit your own games.')
        return redirect(url_for('games.view', game_id=game_id))
    
    round_id = request.form.get('round_id', type=int)
    round_order = request.form.get('round_order', type=int, default=1)
    
    if not round_id:
        flash('Please select a round.')
        return redirect(url_for('games.edit', game_id=game_id))
    
    # Check if round already exists in game
    existing = GameRound.query.filter_by(game_id=game_id, round_id=round_id).first()
    if existing:
        flash('This round is already in the game.')
        return redirect(url_for('games.edit', game_id=game_id))
    
    # Add round to game
    game_round = GameRound(
        game_id=game_id,
        round_id=round_id,
        round_order=round_order
    )
    db.session.add(game_round)
    db.session.commit()
    
    flash('Round added to game successfully!')
    return redirect(url_for('games.edit', game_id=game_id))

@bp.route('/<int:game_id>/remove-round/<int:round_id>')
@login_required
def remove_round(game_id, round_id):
    game = Game.query.get_or_404(game_id)
    
    # Check if user owns this game
    if game.created_by != current_user.id:
        flash('You can only edit your own games.')
        return redirect(url_for('games.view', game_id=game_id))
    
    game_round = GameRound.query.filter_by(game_id=game_id, round_id=round_id).first()
    if game_round:
        db.session.delete(game_round)
        db.session.commit()
        flash('Round removed from game successfully!')
    
    return redirect(url_for('games.edit', game_id=game_id))

@bp.route('/list')
def list():
    page = request.args.get('page', 1, type=int)
    games = Game.query.filter_by(is_active=True).order_by(Game.game_date.desc()).paginate(
        page=page, per_page=current_app.config['GAMES_PER_PAGE'], error_out=False)
    
    return render_template('games/list.html', 
                         title='All Games',
                         games=games)

@bp.route('/my-games')
@login_required
def my_games():
    page = request.args.get('page', 1, type=int)
    games = Game.query.filter_by(created_by=current_user.id, is_active=True).order_by(Game.game_date.desc()).paginate(
        page=page, per_page=current_app.config['GAMES_PER_PAGE'], error_out=False)
    
    return render_template('games/my_games.html', 
                         title='My Games',
                         games=games)

@bp.route('/upcoming')
def upcoming():
    """Show upcoming games (future dates)"""
    page = request.args.get('page', 1, type=int)
    today = datetime.now().date()
    games = Game.query.filter(
        Game.game_date >= today,
        Game.is_active == True
    ).order_by(Game.game_date.asc()).paginate(
        page=page, per_page=current_app.config['GAMES_PER_PAGE'], error_out=False)
    
    return render_template('games/upcoming.html', 
                         title='Upcoming Games',
                         games=games)

@bp.route('/archive')
def archive():
    """Show past games"""
    page = request.args.get('page', 1, type=int)
    today = datetime.now().date()
    games = Game.query.filter(
        Game.game_date < today,
        Game.is_active == True
    ).order_by(Game.game_date.desc()).paginate(
        page=page, per_page=current_app.config['GAMES_PER_PAGE'], error_out=False)
    
    return render_template('games/archive.html', 
                         title='Game Archive',
                         games=games)
