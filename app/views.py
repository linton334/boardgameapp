from flask import render_template,redirect,flash,request
from app import app, models, db
from .forms import LoginForm, RegisterForm, ChangePassForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required, current_user, logout_user

@app.route('/', methods=['GET'])
def boardgame():
    resultCount = 25
    page = request.args.get('page', 1, type=int)
    data = models.boardGame.query.paginate(page,per_page=resultCount)
    return render_template('boardgames.html', title='BG Browser', current_user=current_user, data=data)

@app.route('/add/<int:game_id>', methods=['POST'])
def add_to_collection(game_id):
    user = current_user
    game = models.boardGame.query.filter_by(id = game_id).first()
    user.boardGames.append(game)
    print("game appended")
    db.session.commit()
    return redirect("/profile")


@app.route('/login')
def login():
    form=RegisterForm()
    loginForm=LoginForm()
    return render_template('login.html', title='Login', form=form, loginForm=loginForm, current_user=current_user)

@app.route('/login', methods=['POST'])
def login_post():
    if current_user.is_authenticated:
        print("hi")
        return redirect('/profile')
    form=RegisterForm()
    loginForm=LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        userEmail = models.userAccount.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        userUsername = models.userAccount.query.filter_by(username=username).first() # if this returns a user, then the username already exists in database
        if userEmail: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return render_template('login.html', title='Login', form=form, loginForm=loginForm, current_user=current_user)


        elif userUsername: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Username already exists')
            return render_template('login.html', title='Login', form=form, loginForm=loginForm, current_user=current_user)

        else:
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = models.userAccount(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!')
            return redirect('/login')

    email = loginForm.email.data
    password = loginForm.password.data
    remember = True if loginForm.remember.data else False
    user = models.userAccount.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect Login')
        return redirect('/login')
    login_user(user, remember=remember)
    return redirect('/profile')

@app.route('/profile')
@login_required
def profile():
    form = ChangePassForm()
    data = current_user.boardGames
    name = current_user.username
    return render_template('profile.html', data=data, name=name, form=form)

@app.route('/profile', methods=['POST'])
@login_required
def passChange():
    form = ChangePassForm()
    currentPass = form.oldpassword.data
    changePass = form.password.data
    if not check_password_hash(current_user.password, currentPass):
        flash('Incorrect Current Password')
        return redirect('/profile')
    current_user.password=generate_password_hash(changePass, method='sha256')
    flash("Password changed!")
    db.session.commit()
    return redirect('/profile')


@app.route('/profile/remove/<int:game_id>', methods=['POST'])
@login_required
def removeGame(game_id):
    game = models.boardGame.query.filter_by(id=game_id).first()
    current_user.boardGames.remove(game)
    db.session.commit()
    return redirect("/profile")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

