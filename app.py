from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Tablet, Leader, Record
from forms import LoginForm, IssueForm
from datetime import date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('issue_tablet'))
        flash('Неверный логин или пароль')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def issue_tablet():
    form = IssueForm()
    form.tablet.choices = [(t.id, t.number) for t in Tablet.query.all()]
    if request.method == 'GET':
        form.issue_date.data = date.today()

    if form.validate_on_submit():
        leader_name = form.leader.data
        leader = Leader.query.filter_by(full_name=leader_name).first()
        if not leader:
            leader = Leader(full_name=leader_name)
            db.session.add(leader)
            db.session.commit()

        record = Record(
            tablet_id=form.tablet.data,
            leader_id=leader.id,
            brigade_number=form.brigade_number.data,
            issue_date=form.issue_date.data,
            added_by=current_user.username
        )
        db.session.add(record)
        db.session.commit()
        flash('Запись успешно добавлена.')
        return redirect(url_for('issue_tablet'))

    return render_template('issue_form.html', form=form)

@app.route('/records')
@login_required
def view_records():
    show_invalid = request.args.get('show_invalid') == '1'
    base_query = Record.query

    if current_user.role != 'admin' and not show_invalid:
        today = date.today()
        yesterday = today - timedelta(days=1)
        base_query = base_query.filter(Record.issue_date.in_([today, yesterday]))

    if not show_invalid:
        base_query = base_query.filter(Record.is_invalid == False)

    records = base_query.order_by(Record.issue_date.desc()).all()
    return render_template('records.html', records=records, show_invalid=show_invalid, user=current_user)

@app.route('/invalidate/<int:record_id>')
@login_required
def invalidate_record(record_id):
    if current_user.role not in ['editor', 'admin']:
        flash('Недостаточно прав.')
        return redirect(url_for('view_records'))
    record = Record.query.get(record_id)
    if record:
        record.is_invalid = True
        db.session.commit()
    return redirect(url_for('view_records'))

@app.route('/delete/<int:record_id>')
@login_required
def delete_record(record_id):
    if current_user.role != 'admin':
        flash('Только администратор может удалять записи.')
        return redirect(url_for('view_records'))
    record = Record.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
    return redirect(url_for('view_records'))

if __name__ == '__main__':
    app.run(debug=True)
