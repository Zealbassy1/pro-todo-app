import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import abort

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Redirect to login page if user is not logged in
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configure the database and secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with our app
db = SQLAlchemy(app)
# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# --- DATABASE MODELS ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    todos = db.relationship('Todo', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.content}>'

# --- FORMS ---
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TodoForm(FlaskForm):
    content = StringField('Todo Item', validators=[DataRequired()])
    submit = SubmitField('Add Todo')

# --- ROUTES ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user) # This is the key line!
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            # We will redirect to the main todo page later
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(content=form.content.data, owner=current_user)
        db.session.add(new_todo)
        db.session.commit()
        flash('Your new to-do has been added!', 'success')
        return redirect(url_for('dashboard'))

    todos = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', name=current_user.username, form=form, todos=todos)

@app.route('/todo/update/<int:todo_id>')
@login_required
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.owner != current_user:
        abort(403) # Forbidden
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/todo/delete/<int:todo_id>')
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if todo.owner != current_user:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash('Your to-do has been deleted.', 'success')
    return redirect(url_for('dashboard'))
    
# This allows you to run the app directly
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)