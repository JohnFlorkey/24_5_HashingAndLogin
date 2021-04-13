from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = 'notmuchofasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def root():
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()

    if form.validate_on_submit():
        new_user = User.register(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(new_user)
        db.session.commit()

        session['username'] = new_user.username
        return redirect('/secret')
    else:
        return render_template('user_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data
        )
        if user:
            session['username'] = user.username
            return redirect('/secret')
        else:
            return render_template('login_form.html', form=form)
    else:
        return render_template('login_form.html', form=form)


@app.route('/secret', methods=['GET'])
def secret():
    if 'username' not in session:
        flash("You must be logged in to view!")
        return redirect('/login')
    else:
        return render_template('secret.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return redirect('/')
