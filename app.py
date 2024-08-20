import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, session, g 
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm, UserEditForm
from models import db, User, connect_db

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
foodieappsecretkey = os.environ.get('SECRET_KEY', "it's a secret")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SUPABASE_DB_URL', 'postgresql:///foodie_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.before_request 
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        flash("Invalid credentials.", 'danger')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    return redirect('/')

@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = UserEditForm(obj=g.user)
    if form.validate_on_submit():
        if User.authenticate(g.user.username, form.password.data):
            g.user.username = form.username.data
            g.user.email = form.email.data
            g.user.image_url = form.image_url.data or User.image_ur.default.arg
            g.user.header_image_url = form.header_image_url.data
            g.user.bio = form.bio.data
            db.session.commit()
            flash("Profile updated.", "success")
            return redirect(f"/users/{g.user.id}")
        else:
            flash("Incorrect password, please try again.", "danger")
            return redirect('/')
    return render_template('users/edit.html', form=form)

@app.route('/')
def homepage():
    """Show homepage."""
    if g.user:
        return render_template('home.html')
    else:
        return render_template('home-anon.html')
