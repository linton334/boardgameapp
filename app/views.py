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

#when the user tries to add a game to their collection
@app.route('/add/<int:game_id>', methods=['POST'])
#the clicked game id is passed in
def add_to_collection(game_id):
    user = current_user
    game = models.boardGame.query.filter_by(id = game_id).first()
    #iterate through all the games in the user's collection
    for userGames in user.boardGames:
        #if its already in their collection then..
        if userGames.title == game.title:
            #give them a promt and send info log
            app.logger.info("%s already in %s's collection", game.title, user.username)
            flash("Game already in collection!")
            return redirect("/")
    user.boardGames.append(game)
    #increment the saves value for that game by 1 (one more person added it to their account)
    game.saves+=1
    app.logger.info('%s added %s', user.username, game.title)
    db.session.commit()
    return redirect("/")

#Login page if no methods are being used (first loaded)
@app.route('/login')
def login():
    form=RegisterForm()
    loginForm=LoginForm()
    return render_template('login.html', title='Login', form=form, loginForm=loginForm, current_user=current_user)

#Login Page if a submit button is pressed
@app.route('/login', methods=['POST'])
def login_post():
    #To make sure a logged in user cant access the login page and create problems
    if current_user.is_authenticated:
        app.logger.warning('%s tried accessing /login when logged in.', current_user.username)
        return redirect('/profile')
    #get forms for use
    form=RegisterForm()
    loginForm=LoginForm()
    #If the registration submit button is pressed then..
    if form.validate_on_submit():
        #get data from form
        username = form.username.data
        email = form.email.data
        password = form.password.data
        userEmail = models.userAccount.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        userUsername = models.userAccount.query.filter_by(username=username).first() # if this returns a user, then the username already exists in database
        if userEmail: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            app.logger.info('Email already in database')
            return render_template('login.html', title='Login', form=form, loginForm=loginForm, current_user=current_user)


        elif userUsername: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Username already exists')
            app.logger.info('Username already in database')
            return render_template('login.html', title='Login', form=form, loginForm=loginForm, current_user=current_user)

        else:
            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = models.userAccount(username=username, email=email, password=generate_password_hash(password, method='sha256'))
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            app.logger.info('%s created an account', new_user.username)
            flash('Account Created!')
            return redirect('/login')

    email = loginForm.email.data
    password = loginForm.password.data
    #did the user tick the remember me button?
    remember = True if loginForm.remember.data else False
    #try to find an account with that email
    user = models.userAccount.query.filter_by(email=email).first()
    #if the email isnt in the database or the password is wrong for that email then..
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect Login')
        return redirect('/login')
    #if login is correct then login the user with the remember me value being true or false
    login_user(user, remember=remember)
    app.logger.info('%s logged in successfully', user.username)
    return redirect('/profile')

@app.route('/profile')
@login_required
def profile():
    form = ChangePassForm()
    data = current_user.boardGames
    name = current_user.username
    return render_template('profile.html', data=data, name=name, form=form)

#if the user clicks the change password submit button
@app.route('/profile', methods=['POST'])
@login_required
def passChange():
    form = ChangePassForm()
    currentPass = form.oldpassword.data
    changePass = form.password.data
    #is the current password correct?
    if not check_password_hash(current_user.password, currentPass):
        flash('Incorrect Current Password')
        return redirect('/profile')
    #hash the new password and set it as the new password
    current_user.password=generate_password_hash(changePass, method='sha256')
    app.logger.info('%s changed their password', current_user.username)
    flash("Password changed!")
    db.session.commit()
    return redirect('/profile')

#if the user removes a game from their collection
@app.route('/profile/remove/<int:game_id>', methods=['POST'])
@login_required
def removeGame(game_id):
    #query the game from the database
    game = models.boardGame.query.filter_by(id=game_id).first()
    #if it exists (error checking)
    if game:
        current_user.boardGames.remove(game)
        app.logger.info('%s removed %s', current_user.username, game.title)
        game.saves-=1
        db.session.commit()
    else:
        app.logger.warning("%s tried to access game %s somehow",current_user.username,game_id)
    return redirect("/profile")

@app.route('/logout')
@login_required
def logout():
    app.logger.info('%s logged out successfully', current_user.username)
    logout_user()
    return redirect('/')

