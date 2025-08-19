import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Round, Question
from app.forms import RoundForm, QuestionForm

bp = Blueprint('rounds', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_unique_title(base_title):
    """Generate unique title by appending number if needed"""
    title = base_title
    counter = 1
    while Round.query.filter_by(title=title).first() is not None:
        title = f"{base_title} {counter}"
        counter += 1
    return title

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RoundForm()
    if form.validate_on_submit():
        # Handle file upload
        attachment_path = None
        if form.attachment.data:
            file = form.attachment.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Create unique filename
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
                    filename = f"{base}_{counter}{ext}"
                    counter += 1
                
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                attachment_path = filename
        
        # Create round with unique title
        unique_title = get_unique_title(form.title.data)
        round_obj = Round(
            title=unique_title,
            round_label=form.round_label.data,
            created_by=current_user.id,
            attachment_path=attachment_path
        )
        db.session.add(round_obj)
        db.session.commit()
        
        flash(f'Round "{unique_title}" created successfully!')
        return redirect(url_for('rounds.add_questions', round_id=round_obj.id))
    
    return render_template('rounds/create.html', title='Create Round', form=form)

@bp.route('/<int:round_id>/questions', methods=['GET', 'POST'])
@login_required
def add_questions(round_id):
    round_obj = Round.query.get_or_404(round_id)
    
    # Check if user owns this round
    if round_obj.created_by != current_user.id:
        flash('You can only edit your own rounds.')
        return redirect(url_for('rounds.view', round_id=round_id))
    
    if request.method == 'POST':
        # Handle dynamic question addition
        question_texts = request.form.getlist('question_text')
        answer_texts = request.form.getlist('answer_text')
        points_list = request.form.getlist('points')
        
        # Clear existing questions
        Question.query.filter_by(round_id=round_id).delete()
        
        # Add new questions
        for i, (q_text, a_text, points) in enumerate(zip(question_texts, answer_texts, points_list), 1):
            if q_text.strip() and a_text.strip():  # Only add non-empty questions
                question = Question(
                    round_id=round_id,
                    question_text=q_text.strip(),
                    answer_text=a_text.strip(),
                    question_number=i,
                    points=int(points) if points.isdigit() else 1
                )
                db.session.add(question)
        
        db.session.commit()
        flash('Questions added successfully!')
        return redirect(url_for('rounds.view', round_id=round_id))
    
    # Get existing questions
    questions = round_obj.questions.order_by(Question.question_number).all()
    
    return render_template('rounds/add_questions.html', 
                         title=f'Add Questions - {round_obj.title}',
                         round_obj=round_obj,
                         questions=questions)

@bp.route('/<int:round_id>')
def view(round_id):
    round_obj = Round.query.get_or_404(round_id)
    questions = round_obj.questions.order_by(Question.question_number).all()
    return render_template('rounds/view.html', 
                         title=round_obj.title,
                         round_obj=round_obj,
                         questions=questions)

@bp.route('/list')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    rounds = Round.query.filter_by(is_active=True).order_by(Round.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ROUNDS_PER_PAGE'], error_out=False)
    
    return render_template('rounds/list.html', 
                         title='All Rounds',
                         rounds=rounds)

@bp.route('/my-rounds')
@login_required
def my_rounds():
    page = request.args.get('page', 1, type=int)
    rounds = Round.query.filter_by(created_by=current_user.id, is_active=True).order_by(Round.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ROUNDS_PER_PAGE'], error_out=False)
    
    return render_template('rounds/my_rounds.html', 
                         title='My Rounds',
                         rounds=rounds)
