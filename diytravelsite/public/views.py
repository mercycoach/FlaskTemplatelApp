# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from diytravelsite.extensions import login_manager
from diytravelsite.public.forms import LoginForm
from diytravelsite.user.forms import RegisterForm
from diytravelsite.user.models import User
from diytravelsite.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def index():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/index.html', form=form)

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('public/login.html', title='Sign In', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data, password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)

@blueprint.route('/dashboard/')
def dashboard():
    return render_template('public/dashboard.html', title='Dashboard')

@blueprint.route('/table_list/')
def table_list():
    return render_template('public/table_list.html', title='table_list')

@blueprint.route('/typography/')
def typography():
    return render_template('public/typography.html', title='Typography')

@blueprint.route('/icons/')
def icons():
    return render_template('public/icons.html', title='Icons')

@blueprint.route('/maps/')
def maps():
    return render_template('public/maps.html', title='Maps')

@blueprint.route('/notifications/')
def notifications():
    return render_template('public/notifications.html', title='Notifications')

@blueprint.route('/user_profile/')
def user_profile():
    return render_template('public/user_profile.html', title='User Profile')

