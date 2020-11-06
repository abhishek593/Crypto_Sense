from flask import Blueprint, render_template, redirect, request, url_for, flash, abort, current_app
from flask_login import login_user, login_required, logout_user, current_user
from app.models import UserProfile
from app.accounts.forms import LoginForm, RegistrationForm, ResetPasswordForm, SendResetPasswordRequestForm
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.send_email import send_email

accounts_blueprint = Blueprint('accounts', __name__, template_folder='templates/accounts')


@accounts_blueprint.route('/welcome')
@login_required
def welcome_user():
    return render_template('dashboard.html')


@accounts_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!')
    return redirect(url_for('accounts.welcome_user'))


@accounts_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accounts.welcome_user'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully')
            nxt = request.args.get('next')
            if nxt is None or nxt[0] == '/':
                nxt = url_for('accounts.welcome_user')

            return redirect(nxt)
        else:
            flash("You are not valid user!")
    return render_template('login.html', form=form)


@accounts_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('accounts.welcome_user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        # date_of_birth = form.date_of_birth.data or None
        date_of_birth = None
        first_name = form.first_name.data
        last_name = form.last_name.data or None
        password = form.password.data
        user = UserProfile(username=username, email=email, first_name=first_name,
                           password=password, last_name=last_name, date_of_birth=date_of_birth)
        db.session.add(user)
        db.session.commit()
        token = user.get_reset_password_token()
        send_email('Activate your account',
                   sender=current_app.config['ADMINS'][0],
                   recipients=[user.email],
                   text_body=render_template('account_activate.txt', user=user, token=token),
                   html_body=render_template('account_activate_email_format.html', user=user, token=token))
        flash('Thanks for registering with us!Please check you mail for activating you account.')
        return redirect(url_for('accounts.login'))
    else:
        print(form.errors)
    return render_template('register.html', form=form)


@accounts_blueprint.route('/activate_account/<token>', methods=['GET', 'POST'])
def activate_account(token):
    if current_user.is_authenticated:
        return redirect(url_for('accounts.welcome_user'))
    user = UserProfile.verify_reset_password_token(token=token)
    if user is not None:
        user.is_active = True
        db.session.add(user)
        db.session.commit()
        flash('Your account is activated.')
    else:
        flash('Invalid Token. Please obtain a new token.')
    return render_template('account_activate.html')


@accounts_blueprint.route('/password_reset_request', methods=['GET', 'POST'])
def send_password_reset_email():
    form = SendResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = UserProfile.query.filter_by(email=email).first()
        if user is not None:
            token = user.get_reset_password_token()
            send_email('Reset Your Password',
                       sender=current_app.config['ADMINS'][0],
                       recipients=[user.email],
                       text_body=render_template('reset_password.txt', user=user, token=token),
                       html_body=render_template('reset_password_email_format.html', user=user, token=token))
            return redirect(url_for('accounts.login'))
        else:
            flash('This email is not registered with us.')
    return render_template('send_reset_password_request.html', form=form)


@accounts_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('accounts.welcome_user'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = UserProfile.verify_reset_password_token(token=token)
        if user is not None:
            password = form.password.data
            password2 = form.password_confirm.data
            if password and password2 and password == password2:
                user.password_hash = generate_password_hash(password)
                db.session.commit()
                flash('Your password has been reset.')
                return redirect(url_for('accounts.login'))
            else:
                flash('Passwords does not match.')
                form = ResetPasswordForm()
                return render_template('reset_password.html', form=form)
        else:
            flash('Invalid Token. Please obtain a new token.')
            return redirect(url_for('accounts.login'))
    return render_template('reset_password.html', form=form)
