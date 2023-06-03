from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from website.models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])  
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Đăng nhập thành công!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Sai pass rồi thằng ngu.', category='error')
        else:
            flash('Email không tồn tại.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Quay về login
    return redirect(url_for('auth.login'))

# GUI đăng ký
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email đã tồn tại.', category='error')
        elif len(email) < 1:
            flash('Email không được ngắn hơn 1 ký tự.', category='error')
        elif len(first_name) < 1:
            flash('Tên không được ngắn hơn 1 ký tự.', category='error')
        elif password1 != password2:
            flash('Mật khẩu không khớp.', category='error')
        elif len(password1) < 1:
            flash('Mật khẩu không được ngắn hơn 1 ký tự.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Tạo thành công!', category='success')
            return redirect(url_for('views.home'))
    return render_template('signup.html', user=current_user)