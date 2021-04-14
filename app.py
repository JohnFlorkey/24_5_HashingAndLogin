from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import UserForm, LoginForm, AddFeedback
from utilities import is_authorized


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
        return redirect(f'/users/{new_user.username}')
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
            return redirect(f'/users/{user.username}')
        else:
            return render_template('login_form.html', form=form)
    else:
        return render_template('login_form.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('/')


@app.route('/users/<username>', methods=['GET'])
def user_detail(username):
    if is_authorized(username):
        user = User.query.filter_by(username=username).first()
        user_no_pwd = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'feedback': user.feedback
        }
        return render_template('user_detail_form.html', user=user_no_pwd)
    else:
        flash("You must be logged in to view!")
        return redirect('/login')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if is_authorized(username):
        user = User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        logout()
        return redirect('/register')
    else:
        flash("You must be logged in to view!")
        return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    if is_authorized(username):
        form = AddFeedback()
        if form.validate_on_submit():
            new_feedback = Feedback(
                title=form.title.data,
                content=form.content.data,
                username=username)
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('add_feedback_form.html', form=form, username=username)
    else:
        flash("You must be logged in to view!")
        return redirect('/login')


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if is_authorized(feedback.username):
        form = AddFeedback(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data,
            feedback.content = form.content.data

            db.session.commit()
            return redirect(f'/users/{feedback.username}')
        else:
            return render_template('update_feedback_form.html', form=form, feedback=feedback)
    else:
        flash("You must be logged in to view!")
        return redirect('/login')


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    import pdb
    pdb.set_trace()
    feedback = Feedback.query.get_or_404(feedback_id)
    if is_authorized(feedback.username):
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        user = User.query.filter_by(username=feedback.username).first()
        user_no_pwd = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'feedback': user.feedback
        }
        return render_template('user_detail_form.html', user=user_no_pwd)


# @app.route('/secret', methods=['GET'])
# def secret():
#     if 'username' not in session:
#         flash("You must be logged in to view!")
#         return redirect('/login')
#     else:
#         return render_template('secret.html')
