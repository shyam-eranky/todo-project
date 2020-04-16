import functools
from flask import(Blueprint,flash,g,redirect,render_template,request,session,url_for,jsonify,json)
from . import db
from todoapp.models import User, ToDo
from todoapp.forms import TasksForm
from flask_login import current_user, login_required
import pprint as pp

bp = Blueprint('tasks',__name__,url_prefix='/tasks')

@bp.route('/', methods=('GET','POST'))
@bp.route('/index', methods=('GET','POST'))
@login_required
def index():
    tasks = ToDo.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks/index.html',tasks=tasks)

@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = TasksForm()
    if form.validate_on_submit():
        task = ToDo(title=form.title.data,user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Added task {} successfully'.format(task.id))
        return redirect(url_for('tasks.index'))

    return render_template('tasks/create.html',title='Create Task', form=form)

@bp.route("/<int:id>/delete", methods=("POST","DELETE","GET"))
@login_required
def delete(id):
    ToDo.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Deleted task {} successfully'.format(id))
    return redirect(url_for('tasks.index'))
